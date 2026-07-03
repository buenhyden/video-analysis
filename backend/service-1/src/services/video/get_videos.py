"""Video Retrieval Service Module."""

import logging
from typing import cast

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.models.video import Video

logger = logging.getLogger(__name__)


def get_videos(db: Session, skip: int = 0, limit: int = 100) -> list[Video]:
    """비디오 목록을 조회합니다."""
    try:
        return cast("list[Video]", db.query(Video).offset(skip).limit(limit).all())
    except SQLAlchemyError as e:
        logger.error(f"Error fetching videos: {e}")
        return []
