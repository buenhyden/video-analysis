"""Video Deletion Service Module."""

import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.models.video import Video

logger = logging.getLogger(__name__)


def delete_video(db: Session, video_id: int) -> bool:
    """비디오를 삭제합니다."""
    try:
        video = db.query(Video).filter(Video.id == video_id).first()
        if video:
            db.delete(video)
            db.commit()
            logger.info(f"Video deleted: ID {video_id}")
            return True
        else:
            logger.warning(f"Delete failed: Video ID {video_id} not found")
            return False
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to delete video ID {video_id}: {e}")
        raise e
