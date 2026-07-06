"""
Orchestrates the chat endpoint: loads/creates a chat, loads history,
calls the AI service for a reply, persists both turns, and resolves
recommended movie ids back into full Movie objects.
"""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat import Chat, ChatMessage
from app.models.movie import Movie
from app.services.ai_service import generate_chat_reply
from app.services.movie_service import get_candidate_movies_for_chat, get_movies_by_ids

MAX_HISTORY_MESSAGES = 20  # cap how much history we send to the model per turn


async def get_or_create_chat(db: AsyncSession, user_id: uuid.UUID, chat_id: uuid.UUID | None) -> Chat:
    if chat_id is not None:
        stmt = select(Chat).where(Chat.id == chat_id, Chat.user_id == user_id)
        result = await db.execute(stmt)
        chat = result.scalar_one_or_none()
        if chat is not None:
            return chat
        # Falls through to creating a new chat if the given id wasn't found/owned by this user.

    chat = Chat(user_id=user_id)
    db.add(chat)
    await db.flush()  # assigns chat.id without committing yet
    return chat


async def get_recent_history(db: AsyncSession, chat_id: uuid.UUID) -> list[ChatMessage]:
    stmt = (
        select(ChatMessage)
        .where(ChatMessage.chat_id == chat_id)
        .order_by(ChatMessage.created_at.desc())
        .limit(MAX_HISTORY_MESSAGES)
    )
    result = await db.execute(stmt)
    messages = list(result.scalars().all())
    messages.reverse()  # back to chronological order
    return messages


async def handle_user_message(
    db: AsyncSession,
    user_id: uuid.UUID,
    chat_id: uuid.UUID | None,
    user_text: str,
) -> tuple[Chat, ChatMessage, list[Movie]]:
    """
    Full chat turn: persist user message, run AI, persist assistant message.
    Returns (chat, assistant_message, recommended_movies).
    """
    chat = await get_or_create_chat(db, user_id, chat_id)

    user_message = ChatMessage(chat_id=chat.id, role="user", content=user_text)
    db.add(user_message)
    await db.flush()

    history_records = await get_recent_history(db, chat.id)
    history_payload = [{"role": m.role, "content": m.content} for m in history_records if m.role != "system"]

    candidates = await get_candidate_movies_for_chat(db, user_text)

    reply_text, recommended_id_strings = await generate_chat_reply(history_payload, candidates)

    valid_uuids: list[uuid.UUID] = []
    for raw_id in recommended_id_strings:
        try:
            valid_uuids.append(uuid.UUID(raw_id))
        except ValueError:
            continue  # ignore anything the model hallucinated that isn't a real UUID

    recommended_movies = await get_movies_by_ids(db, valid_uuids)
    # Only keep ids that resolved to real movies, preserving order.
    resolved_ids = [m.id for m in recommended_movies]

    assistant_message = ChatMessage(
        chat_id=chat.id,
        role="assistant",
        content=reply_text,
        recommended_movie_ids=resolved_ids,
    )
    db.add(assistant_message)

    # Auto-title new chats from the first user message.
    if chat.title is None:
        chat.title = user_text[:80]

    await db.commit()
    await db.refresh(assistant_message)

    return chat, assistant_message, recommended_movies
