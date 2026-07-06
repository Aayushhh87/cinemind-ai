import hashlib
import logging
import math
import re

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models import Movie

logger = logging.getLogger(__name__)


def search_movies_by_title(db: Session, query: str, limit: int = 20) -> list[Movie]:
    cleaned = query.strip()
    if not cleaned:
        return []

    pattern = f"%{cleaned}%"
    return (
        db.query(Movie)
        .filter(
            or_(
                Movie.title.ilike(pattern),
                Movie.original_title.ilike(pattern),
            )
        )
        .order_by(Movie.popularity.desc().nullslast(), Movie.vote_average.desc().nullslast())
        .limit(limit)
        .all()
    )


def get_movie(db: Session, movie_id) -> Movie | None:
    return db.query(Movie).filter(Movie.id == movie_id).first()


def list_movies(db: Session, limit: int = 20, offset: int = 0) -> tuple[list[Movie], int]:
    total = db.query(func.count(Movie.id)).scalar() or 0
    items = (
        db.query(Movie)
        .order_by(Movie.popularity.desc().nullslast(), Movie.title.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return items, total


def _tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def keyword_relevance(movie: Movie, query: str) -> float:
    tokens = _tokenize(query)
    if not tokens:
        return 0.0

    haystack = " ".join(
        filter(
            None,
            [
                movie.title,
                movie.original_title or "",
                movie.overview or "",
                movie.director or "",
                " ".join(movie.genres or []),
                " ".join(movie.cast_members or []),
            ],
        )
    ).lower()
    doc_tokens = _tokenize(haystack)
    if not doc_tokens:
        return 0.0

    overlap = len(tokens & doc_tokens) / len(tokens)
    title_tokens = _tokenize(movie.title)
    title_overlap = len(tokens & title_tokens) / max(len(tokens), 1)
    return min(1.0, overlap * 0.7 + title_overlap * 0.3)


def mock_embedding(text: str, dimensions: int = 1536) -> list[float]:
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    values: list[float] = []
    seed = int.from_bytes(digest[:8], "big")
    for index in range(dimensions):
        seed = (1103515245 * seed + 12345 + index) & 0x7FFFFFFF
        values.append((seed / 0x7FFFFFFF) * 2 - 1)
    norm = math.sqrt(sum(value * value for value in values)) or 1.0
    return [value / norm for value in values]
