from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    message: str


class HealthResponse(BaseModel):
    status: str
    app: str
    database: str
    chromadb: str


class MovieSummary(ORMModel):
    id: UUID
    title: str
    release_date: date | None = None
    genres: list[str] = Field(default_factory=list)
    vote_average: float | None = None
    poster_url: str | None = None
    overview: str | None = None


class MovieDetail(MovieSummary):
    original_title: str | None = None
    runtime_minutes: int | None = None
    director: str | None = None
    cast_members: list[str] = Field(default_factory=list)
    backdrop_url: str | None = None
    language: str | None = None
    vote_count: int | None = None
    popularity: float | None = None
    external_id: str | None = None
    external_source: str | None = None


class MovieListResponse(BaseModel):
    items: list[MovieSummary]
    total: int


class SemanticSearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    limit: int = Field(default=10, ge=1, le=50)


class SemanticSearchResult(BaseModel):
    movie: MovieSummary
    score: float
    explanation: str


class SemanticSearchResponse(BaseModel):
    query: str
    results: list[SemanticSearchResult]


class ChatCreate(BaseModel):
    title: str | None = Field(default=None, max_length=255)


class ChatSummary(ORMModel):
    id: UUID
    title: str | None = None


class ChatMessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=4000)


class ChatMessageOut(ORMModel):
    id: UUID
    role: str
    content: str
    recommended_movie_ids: list[UUID] = Field(default_factory=list)


class ChatDetail(ORMModel):
    id: UUID
    title: str | None = None
    messages: list[ChatMessageOut] = Field(default_factory=list)
