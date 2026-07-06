import logging

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import hash_password
from app.models import User

logger = logging.getLogger(__name__)


def ensure_demo_user(db: Session) -> User:
    settings = get_settings()
    user = db.query(User).filter(User.email == settings.demo_user_email).first()
    if user:
        return user

    user = User(
        email=settings.demo_user_email,
        password_hash=hash_password("demo-password-not-for-production"),
        display_name="Demo User",
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info("Created demo user: %s", settings.demo_user_email)
    return user
