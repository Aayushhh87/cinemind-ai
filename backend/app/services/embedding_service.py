import logging

from openai import OpenAI
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import Movie
from app.services.movie_service import mock_embedding

logger = logging.getLogger(__name__)


def generate_embedding(text: str) -> list[float]:
    settings = get_settings()
    if settings.openai_api_key:
        try:
            client = OpenAI(api_key=settings.openai_api_key)
            response = client.embeddings.create(
                model=settings.openai_embedding_model,
                input=text,
            )
            return response.data[0].embedding
        except Exception:
            logger.exception("OpenAI embedding failed; falling back to mock embedding")

    return mock_embedding(text)


def movie_document(movie: Movie) -> str:
    return "\n".join(
        filter(
            None,
            [
                f"Title: {movie.title}",
                f"Original title: {movie.original_title}" if movie.original_title else None,
                f"Overview: {movie.overview}" if movie.overview else None,
                f"Genres: {', '.join(movie.genres)}" if movie.genres else None,
                f"Director: {movie.director}" if movie.director else None,
                f"Cast: {', '.join(movie.cast_members)}" if movie.cast_members else None,
            ],
        )
    )


def sync_movie_embedding(db: Session, movie: Movie) -> list[float]:
    vector = generate_embedding(movie_document(movie))
    movie.embedding = vector
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return vector
