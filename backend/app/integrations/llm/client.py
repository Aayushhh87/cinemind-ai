import logging

from openai import OpenAI

from app.core.config import get_settings
from app.models import Movie
from app.models.base import ChatMessage
from app.integrations.llm.prompts import build_fallback_response, build_recommendation_prompt

logger = logging.getLogger(__name__)


def generate_chat_response(
    user_message: str,
    recommended_movies: list[Movie],
    history: list[ChatMessage],
) -> str:
    settings = get_settings()
    if not settings.openai_api_key:
        return build_fallback_response(user_message, recommended_movies)

    messages: list[dict[str, str]] = [
        {"role": "system", "content": build_recommendation_prompt(user_message, recommended_movies)},
    ]
    for item in history[-6:]:
        if item.role in {"user", "assistant"}:
            messages.append({"role": item.role, "content": item.content})
    messages.append({"role": "user", "content": user_message})

    try:
        client = OpenAI(api_key=settings.openai_api_key)
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
            temperature=0.7,
        )
        content = response.choices[0].message.content
        return content or build_fallback_response(user_message, recommended_movies)
    except Exception:
        logger.exception("OpenAI chat completion failed; using fallback response")
        return build_fallback_response(user_message, recommended_movies)
