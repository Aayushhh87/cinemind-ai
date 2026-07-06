import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.movie import MovieOut


class ChatMessageIn(BaseModel):
    """Payload for sending a message to the AI."""

    user_id: uuid.UUID
    chat_id: uuid.UUID | None = Field(
        default=None, description="Existing chat id to continue. Omit to start a new chat."
    )
    message: str = Field(min_length=1, max_length=4000)


class ChatMessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    role: str
    content: str
    created_at: datetime


class ChatResponse(BaseModel):
    """Response returned after posting a message: the chat id, the assistant's
    reply, and any movies the assistant recommended."""

    chat_id: uuid.UUID
    message: ChatMessageOut
    recommended_movies: list[MovieOut] = []


class ChatHistoryOut(BaseModel):
    chat_id: uuid.UUID
    title: str | None = None
    messages: list[ChatMessageOut]
