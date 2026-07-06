import logging

from sqlalchemy.orm import Session

from app.models import Chat, ChatMessage, Movie, User
from app.schemas.common import ChatMessageOut
from app.services.movie_service import keyword_relevance, search_movies_by_title
from app.services.search_service import semantic_search
from app.integrations.llm.client import generate_chat_response

logger = logging.getLogger(__name__)


def create_chat(db: Session, user: User, title: str | None = None) -> Chat:
    chat = Chat(user_id=user.id, title=title or "New chat")
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


def get_chat(db: Session, chat_id, user: User) -> Chat | None:
    return db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user.id).first()


def list_chats(db: Session, user: User, limit: int = 20) -> list[Chat]:
    return (
        db.query(Chat)
        .filter(Chat.user_id == user.id)
        .order_by(Chat.updated_at.desc())
        .limit(limit)
        .all()
    )


def _pick_recommendations(db: Session, user_message: str, limit: int = 5) -> list[Movie]:
    try:
        semantic_results = semantic_search(db, user_message, limit=limit)
        if semantic_results:
            return [result.movie for result in semantic_results]
    except Exception:
        logger.exception("Semantic search failed during chat; falling back to title search")

    title_matches = search_movies_by_title(db, user_message, limit=limit)
    if title_matches:
        return title_matches

    return db.query(Movie).order_by(Movie.popularity.desc().nullslast()).limit(limit).all()


def send_message(db: Session, chat: Chat, content: str) -> tuple[ChatMessage, ChatMessage]:
    user_message = ChatMessage(chat_id=chat.id, role="user", content=content)
    db.add(user_message)
    db.flush()

    history = (
        db.query(ChatMessage)
        .filter(ChatMessage.chat_id == chat.id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )
    recommended = _pick_recommendations(db, content)
    assistant_text = generate_chat_response(content, recommended, history)

    assistant_message = ChatMessage(
        chat_id=chat.id,
        role="assistant",
        content=assistant_text,
        recommended_movie_ids=[movie.id for movie in recommended],
    )
    db.add(assistant_message)

    if not chat.title or chat.title == "New chat":
        chat.title = content[:80]

    db.commit()
    db.refresh(user_message)
    db.refresh(assistant_message)
    return user_message, assistant_message


def message_to_schema(message: ChatMessage) -> ChatMessageOut:
    return ChatMessageOut.model_validate(message)
