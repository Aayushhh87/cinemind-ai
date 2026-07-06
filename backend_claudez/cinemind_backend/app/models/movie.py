import uuid
from datetime import date, datetime

from sqlalchemy import ARRAY, Date, DateTime, Integer, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Movie(Base):
    __tablename__ = "movies"
    __table_args__ = (UniqueConstraint("external_source", "external_id", name="uq_movie_external"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    original_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    overview: Mapped[str | None] = mapped_column(Text, nullable=True)
    release_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    runtime_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    genres: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False, default=list)
    director: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cast_members: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False, default=list)
    poster_url: Mapped[str | None] = mapped_column(String, nullable=True)
    backdrop_url: Mapped[str | None] = mapped_column(String, nullable=True)
    language: Mapped[str | None] = mapped_column(String(10), default="en")
    vote_average: Mapped[float | None] = mapped_column(Numeric(3, 1), nullable=True)
    vote_count: Mapped[int | None] = mapped_column(Integer, default=0)
    popularity: Mapped[float | None] = mapped_column(Numeric(10, 3), default=0)
    external_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    external_source: Mapped[str | None] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # NOTE: the `embedding VECTOR(1536)` column from the SQL schema is intentionally
    # omitted from this ORM model. Wiring up pgvector with SQLAlchemy requires the
    # `pgvector` Python package + extra config; add it later if semantic search is needed.
