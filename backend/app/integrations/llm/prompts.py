from app.models import Movie
from app.models.base import ChatMessage


def build_recommendation_prompt(user_message: str, movies: list[Movie]) -> str:
    if not movies:
        return (
            "You are CineMind AI, a helpful movie recommendation assistant. "
            "The catalog is empty. Apologize briefly and suggest trying a title search."
        )

    lines = [
        "You are CineMind AI, a concise movie recommendation assistant.",
        "Recommend movies from the provided catalog only.",
        "For each pick, include title, release year, and a one-sentence reason.",
        "",
        "Catalog:",
    ]
    for movie in movies:
        year = movie.release_date.year if movie.release_date else "Unknown"
        genres = ", ".join(movie.genres) if movie.genres else "Unknown"
        lines.append(f"- {movie.title} ({year}) | Genres: {genres} | {movie.overview or ''}")

    lines.extend(["", f"User request: {user_message}"])
    return "\n".join(lines)


def build_fallback_response(user_message: str, movies: list[Movie]) -> str:
    if not movies:
        return (
            "I couldn't find matching movies yet. Try searching by title or add seed data to the catalog."
        )

    lines = [f"Here are some picks based on your request: \"{user_message}\"", ""]
    for movie in movies[:5]:
        year = movie.release_date.year if movie.release_date else "Unknown"
        reason = movie.overview or "A strong match from the CineMind catalog."
        lines.append(f"**{movie.title}** ({year}) — {reason[:160]}")
    lines.append("")
    lines.append("_Set OPENAI_API_KEY for richer AI explanations._")
    return "\n".join(lines)
