from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.common import MovieDetail, MovieListResponse, MovieSummary
from app.services.movie_service import get_movie, list_movies, search_movies_by_title

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("", response_model=MovieListResponse)
def list_all_movies(
    q: str | None = Query(default=None, description="Search by movie title"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> MovieListResponse:
    if q:
        items = search_movies_by_title(db, q, limit=limit)
        summaries = [MovieSummary.model_validate(movie) for movie in items]
        return MovieListResponse(items=summaries, total=len(summaries))

    items, total = list_movies(db, limit=limit, offset=offset)
    summaries = [MovieSummary.model_validate(movie) for movie in items]
    return MovieListResponse(items=summaries, total=total)


@router.get("/{movie_id}", response_model=MovieDetail)
def get_movie_detail(movie_id: UUID, db: Session = Depends(get_db)) -> MovieDetail:
    movie = get_movie(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return MovieDetail.model_validate(movie)
