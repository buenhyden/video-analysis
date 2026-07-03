"""Video Creation Service Module."""

import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.models.video import Video
from src.schemas.video import VideoCreate

from .extract_thumbnail import extract_thumbnail

logger = logging.getLogger(__name__)


def create_video(db: Session, video: VideoCreate, user_id: int) -> Video:
    """비디오를 생성합니다."""
    try:
        # Pydantic 모델을 딕셔너리로 변환하여 데이터 조작
        video_data = video.model_dump()

        # 썸네일이 비어있다면 URL 기반 자동 추출 시도
        if not video_data.get("thumbnail"):
            # Mypy fix: use video.url (str) instead of dict.get (Any)
            extracted_thumb = extract_thumbnail(video.url)
            if extracted_thumb:
                video_data["thumbnail"] = extracted_thumb
                logger.info("Thumbnail auto-generated for URL: %s", video_data["url"])
            else:
                # [수정] via.placeholder.com 대신 안정적인 placehold.co 사용
                # 다크 테마용 (배경: #1e293b, 글자: #cbd5e1)
                video_data["thumbnail"] = "https://placehold.co/800x450/1e293b/cbd5e1.png?text=No+Thumbnail"
        # DB 모델 생성
        db_video = Video(**video_data, owner_id=user_id)
        db.add(db_video)
        db.commit()
        db.refresh(db_video)
        logger.info(
            "Video created: %s (ID: %s) by User ID: %s",
            db_video.title,
            db_video.id,
            user_id,
        )
        return db_video
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("Failed to create video '%s': %s", video.title, e)
        raise e
