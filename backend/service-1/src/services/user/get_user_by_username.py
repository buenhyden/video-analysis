"""User Retrieval Service Module."""

import logging
from typing import cast

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.models import User

logger = logging.getLogger(__name__)


def get_user_by_username(db: Session, username: str) -> User | None:
    """사용자 이름을 기반으로 사용자를 조회합니다."""
    try:
        return cast("User | None", db.query(User).filter(User.username == username).first())
    except SQLAlchemyError as e:
        logger.error(f"Error fetching user by username {username}: {e}")
        return None
