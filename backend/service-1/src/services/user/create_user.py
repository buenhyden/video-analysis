"""User Creation Service Module."""

import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.core.security import get_password_hash
from src.models import User
from src.schemas import UserCreate

logger = logging.getLogger(__name__)


def create_user(db: Session, user: UserCreate) -> User:
    """사용자를 생성합니다."""
    try:
        hashed_password = get_password_hash(user.password)
        db_user = User(username=user.username, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to create user {user.username}: {e}")
        raise e
