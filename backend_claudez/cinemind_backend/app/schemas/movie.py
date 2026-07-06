import uuid
from datetime import date

from pydantic import BaseModel, ConfigDict


class MovieOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    original_title: str | None = None
    overview: str | None = None
    release_date: date | None = None
    runtime_minutes: int | None = None
    genres: list[str] = []
    director: str | None = None
    cast_members: list[str] = []
    poster_url: str | None = None
    backdrop_url: str | None = None
    language: str | None = None
    vote_average: float | None = None
    vote_count: int | None = None
    popularity: float | None = None


class MovieSearchResponse(BaseModel):
    query: str
    count: int
    results: list[MovieOut]
