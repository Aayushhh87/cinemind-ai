from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.movie import MovieOut, MovieSearchResponse
from app.services.movie_service import search_movies

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("/search", response_model=MovieSearchResponse)
async def search_movies_endpoint(
    q: str | None = Query(default=None, description="Free-text search over title/overview"),
    genre: str | None = Query(default=None, description="Filter by exact genre, e.g. 'Sci-Fi'"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> MovieSearchResponse:
    """
    Search the movie catalog by free-text query and/or genre.

    At least one of `q` or `genre` is recommended, but if both are omitted this
    falls back to a generic popularity-sorted listing.
    """
    movies = await search_movies(db, query=q, genre=genre, limit=limit, offset=offset)
    return MovieSearchResponse(
        query=q or "",
        count=len(movies),
        results=[MovieOut.model_validate(m) for m in movies],
    )
