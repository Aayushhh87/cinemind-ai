"""
Query helpers for movies: text search for the search endpoint, and a
candidate-pool fetch used by the chat endpoint to ground AI recommendations
in real catalog data.
"""
import uuid

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.movie import Movie


async def search_movies(
    db: AsyncSession,
    query: str | None,
    genre: str | None,
    limit: int,
    offset: int,
) -> list[Movie]:
    """
    Simple keyword + genre search over the movies table.
    Matches on title (case-insensitive substring) and/or genre membership.
    """
    stmt = select(Movie)

    if query:
        like_pattern = f"%{query}%"
        stmt = stmt.where(
            or_(
                Movie.title.ilike(like_pattern),
                Movie.original_title.ilike(like_pattern),
                Movie.overview.ilike(like_pattern),
            )
        )

    if genre:
        stmt = stmt.where(Movie.genres.any(genre))

    stmt = stmt.order_by(Movie.popularity.desc().nullslast()).limit(limit).offset(offset)

    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_candidate_movies_for_chat(
    db: AsyncSession,
    user_message: str,
    limit: int = 25,
) -> list[Movie]:
    """
    Fetches a pool of candidate movies for the AI to choose recommendations from,
    based on naive keyword overlap with the user's message plus general popularity.

    This is intentionally simple for the MVP. Swap this for pgvector cosine-similarity
    search once movie embeddings are populated.
    """
    words = [w.strip().lower() for w in user_message.split() if len(w.strip()) > 3]

    stmt = select(Movie)
    if words:
        conditions = [Movie.title.ilike(f"%{w}%") for w in words]
        conditions += [Movie.overview.ilike(f"%{w}%") for w in words]
        conditions += [Movie.genres.any(w) for w in words]
        stmt = stmt.where(or_(*conditions))

    stmt = stmt.order_by(Movie.popularity.desc().nullslast()).limit(limit)
    result = await db.execute(stmt)
    candidates = list(result.scalars().all())

    if len(candidates) < 5:
        # Not enough keyword matches — top up with generally popular movies so
        # the AI still has something reasonable to work with.
        fallback_stmt = select(Movie).order_by(Movie.popularity.desc().nullslast()).limit(limit)
        fallback_result = await db.execute(fallback_stmt)
        existing_ids = {m.id for m in candidates}
        for movie in fallback_result.scalars().all():
            if movie.id not in existing_ids:
                candidates.append(movie)
            if len(candidates) >= limit:
                break

    return candidates


async def get_movies_by_ids(db: AsyncSession, movie_ids: list[uuid.UUID]) -> list[Movie]:
    if not movie_ids:
        return []
    stmt = select(Movie).where(Movie.id.in_(movie_ids))
    result = await db.execute(stmt)
    movies = {m.id: m for m in result.scalars().all()}
    # Preserve the order the AI recommended them in.
    return [movies[mid] for mid in movie_ids if mid in movies]
