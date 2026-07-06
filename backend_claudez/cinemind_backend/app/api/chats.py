import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.chat import Chat, ChatMessage
from app.schemas.chat import ChatHistoryOut, ChatMessageIn, ChatMessageOut, ChatResponse
from app.schemas.movie import MovieOut
from app.services.chat_service import handle_user_message

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("", response_model=ChatResponse)
async def post_chat_message(
    payload: ChatMessageIn,
    db: AsyncSession = Depends(get_db),
) -> ChatResponse:
    """
    Send a message to CineMind AI.

    - If `chat_id` is omitted, a new chat is created for the user.
    - If `chat_id` is provided, the message is appended to that existing chat
      (must belong to `user_id`, otherwise a new chat is started transparently).

    Returns the assistant's reply along with any movies it recommended.
    """
    try:
        chat, assistant_message, recommended_movies = await handle_user_message(
            db=db,
            user_id=payload.user_id,
            chat_id=payload.chat_id,
            user_text=payload.message,
        )
    except RuntimeError as exc:
        # Raised by ai_service if ANTHROPIC_API_KEY is missing/misconfigured.
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return ChatResponse(
        chat_id=chat.id,
        message=ChatMessageOut.model_validate(assistant_message),
        recommended_movies=[MovieOut.model_validate(m) for m in recommended_movies],
    )


@router.get("/{chat_id}", response_model=ChatHistoryOut)
async def get_chat_history(
    chat_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> ChatHistoryOut:
    """Fetch the full message history for a given chat."""
    stmt = select(Chat).where(Chat.id == chat_id)
    result = await db.execute(stmt)
    chat = result.scalar_one_or_none()
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")

    msg_stmt = select(ChatMessage).where(ChatMessage.chat_id == chat_id).order_by(ChatMessage.created_at)
    msg_result = await db.execute(msg_stmt)
    messages = list(msg_result.scalars().all())

    return ChatHistoryOut(
        chat_id=chat.id,
        title=chat.title,
        messages=[ChatMessageOut.model_validate(m) for m in messages],
    )
