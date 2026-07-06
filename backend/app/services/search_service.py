import logging

from sqlalchemy.orm import Session

from app.integrations.chromadb.client import get_movies_collection
from app.integrations.chromadb.embeddings import index_all_movies, query_movies
from app.models import Movie
from app.schemas.common import MovieSummary, SemanticSearchResult
from app.services.embedding_service import generate_embedding, movie_document
from app.services.movie_service import keyword_relevance

logger = logging.getLogger(__name__)


def semantic_search(db: Session, query: str, limit: int = 10) -> list[SemanticSearchResult]:
    collection = get_movies_collection()
    if collection is not None:
        try:
            chroma_results = query_movies(collection, query, limit=limit)
            if chroma_results:
                movie_ids = [movie_id for movie_id, _ in chroma_results]
                movies = db.query(Movie).filter(Movie.id.in_(movie_ids)).all()
                movie_map = {movie.id: movie for movie in movies}
                results: list[SemanticSearchResult] = []
                for movie_id, score in chroma_results:
                    movie = movie_map.get(movie_id)
                    if movie:
                        results.append(
                            SemanticSearchResult(
                                movie=MovieSummary.model_validate(movie),
                                score=score,
                                explanation=f"Semantic match for themes and description in '{movie.title}'.",
                            )
                        )
                if results:
                    return results
        except Exception:
            logger.exception("ChromaDB query failed; falling back to keyword search")

    return _keyword_semantic_fallback(db, query, limit)


def _keyword_semantic_fallback(db: Session, query: str, limit: int) -> list[SemanticSearchResult]:
    movies = db.query(Movie).all()
    scored: list[tuple[Movie, float]] = []
    for movie in movies:
        score = keyword_relevance(movie, query)
        if score > 0:
            scored.append((movie, score))
    scored.sort(key=lambda item: item[1], reverse=True)

    return [
        SemanticSearchResult(
            movie=MovieSummary.model_validate(movie),
            score=score,
            explanation=f"Keyword overlap match for '{movie.title}'.",
        )
        for movie, score in scored[:limit]
    ]


def sync_movies_to_chroma(db: Session) -> int:
    collection = get_movies_collection()
    if collection is None:
        logger.warning("ChromaDB unavailable; skipping movie index sync")
        return 0
    return index_all_movies(db, collection)


def ensure_movie_embeddings(db: Session) -> int:
    movies = db.query(Movie).filter(Movie.embedding.is_(None)).all()
    count = 0
    for movie in movies:
        movie.embedding = generate_embedding(movie_document(movie))
        db.add(movie)
        count += 1
    if count:
        db.commit()
    return count
