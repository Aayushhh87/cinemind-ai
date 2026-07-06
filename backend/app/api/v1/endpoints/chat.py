from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.init_db import ensure_demo_user
from app.schemas.common import (
    ChatCreate,
    ChatDetail,
    ChatMessageCreate,
    ChatMessageOut,
    ChatSummary,
)
from app.services.chat_service import create_chat, get_chat, list_chats, message_to_schema, send_message

router = APIRouter(prefix="/chats", tags=["chats"])


def _demo_user(db: Session):
    return ensure_demo_user(db)


@router.get("", response_model=list[ChatSummary])
def get_chats(db: Session = Depends(get_db)) -> list[ChatSummary]:
    user = _demo_user(db)
    chats = list_chats(db, user)
    return [ChatSummary.model_validate(chat) for chat in chats]


@router.post("", response_model=ChatSummary, status_code=201)
def start_chat(payload: ChatCreate, db: Session = Depends(get_db)) -> ChatSummary:
    user = _demo_user(db)
    chat = create_chat(db, user, title=payload.title)
    return ChatSummary.model_validate(chat)


@router.get("/{chat_id}", response_model=ChatDetail)
def get_chat_detail(chat_id: UUID, db: Session = Depends(get_db)) -> ChatDetail:
    user = _demo_user(db)
    chat = get_chat(db, chat_id, user)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return ChatDetail(
        id=chat.id,
        title=chat.title,
        messages=[message_to_schema(message) for message in chat.messages],
    )


@router.post("/{chat_id}/messages", response_model=list[ChatMessageOut])
def post_message(
    chat_id: UUID,
    payload: ChatMessageCreate,
    db: Session = Depends(get_db),
) -> list[ChatMessageOut]:
    user = _demo_user(db)
    chat = get_chat(db, chat_id, user)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    user_message, assistant_message = send_message(db, chat, payload.content)
    return [
        message_to_schema(user_message),
        message_to_schema(assistant_message),
    ]
