"""
Thin wrapper around the Anthropic API for CineMind AI's chat feature.

Strategy for the MVP:
1. Pull a candidate pool of movies from Postgres (simple keyword/genre filter,
   since pgvector semantic search is not wired up yet).
2. Ask Claude to have a natural conversation with the user AND, if relevant,
   pick movie titles from the candidate pool to recommend.
3. Parse Claude's structured JSON output to know which movies (by id) to
   attach to the response, and what text to show the user.
"""
import json
import logging

from anthropic import AsyncAnthropic

from app.core.config import get_settings
from app.models.movie import Movie

logger = logging.getLogger(__name__)
settings = get_settings()

_client: AsyncAnthropic | None = None


def get_anthropic_client() -> AsyncAnthropic:
    global _client
    if _client is None:
        if not settings.anthropic_api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not set. Add it to your .env file to enable the chat endpoint."
            )
        _client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    return _client


SYSTEM_PROMPT = """You are CineMind AI, a friendly and knowledgeable movie recommendation assistant.

You will be given:
- The recent conversation history with a user.
- A list of candidate movies (with id, title, overview, genres, release year) pulled from the catalog.

Your job:
1. Respond conversationally and helpfully to the user's message.
2. If, and only if, recommending movies is relevant to what the user said, choose up to 5 movies
   FROM THE CANDIDATE LIST ONLY (never invent movies, never use movies not in the candidate list).
3. If no candidate movies fit, recommended_movie_ids should be an empty list. It's fine to say you
   don't have a good match in the catalog.

Respond ONLY with a single valid JSON object, no markdown fences, no preamble, in this exact shape:
{"reply": "<your conversational reply as plain text>", "recommended_movie_ids": ["<uuid>", "..."]}
"""


def _format_candidates(movies: list[Movie]) -> str:
    if not movies:
        return "No candidate movies available."
    lines = []
    for m in movies:
        year = m.release_date.year if m.release_date else "unknown year"
        genres = ", ".join(m.genres) if m.genres else "unspecified genre"
        overview = (m.overview or "")[:200]
        lines.append(f"- id={m.id} | {m.title} ({year}) | genres: {genres} | {overview}")
    return "\n".join(lines)


async def generate_chat_reply(
    history: list[dict],
    candidate_movies: list[Movie],
) -> tuple[str, list[str]]:
    """
    Calls Claude with the conversation history + candidate movie pool.

    Args:
        history: list of {"role": "user"|"assistant", "content": str}, oldest first.
        candidate_movies: Movie ORM objects to choose recommendations from.

    Returns:
        (reply_text, recommended_movie_id_strings)
    """
    client = get_anthropic_client()

    candidates_block = _format_candidates(candidate_movies)
    context_message = (
        f"CANDIDATE MOVIES:\n{candidates_block}\n\n"
        "Now respond to the user's latest message, following the JSON output format exactly."
    )

    messages = history + [{"role": "user", "content": context_message}]

    response = await client.messages.create(
        model=settings.anthropic_model,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages,
    )

    raw_text = "".join(block.text for block in response.content if block.type == "text").strip()

    try:
        # Defensively strip markdown fences if the model adds them anyway.
        cleaned = raw_text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        parsed = json.loads(cleaned)
        reply = parsed.get("reply", "").strip()
        movie_ids = parsed.get("recommended_movie_ids", []) or []
        if not isinstance(movie_ids, list):
            movie_ids = []
        return reply or "Sorry, I didn't quite catch that — could you rephrase?", [str(i) for i in movie_ids]
    except (json.JSONDecodeError, AttributeError) as exc:
        logger.warning("Failed to parse Claude JSON response: %s | raw=%s", exc, raw_text)
        # Fall back to returning the raw text with no recommendations rather than failing the request.
        return raw_text or "Sorry, something went wrong generating a response.", []
