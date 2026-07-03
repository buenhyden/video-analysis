"""service-1: SQLAlchemy Video Repository Implementation.

Domain의 VideoRepository 인터페이스를 구현한다.
ORM ↔ Domain 변환(Mapper)을 담당한다.
"""

import logging
from datetime import datetime

from sqlalchemy.orm import Session

from src.domain.video.video import Video
from src.domain.video.video_repository import VideoRepository
from src.infrastructure.orm.video_orm import VideoORM

logger = logging.getLogger(__name__)


def _to_domain(row: VideoORM) -> Video:
    """ORM → Domain 변환."""
    return Video(
        id=row.id,
        title=row.title,
        category=row.category,
        description=row.description,
        url=row.url,
        owner_id=row.owner_id,
        thumbnail=row.thumbnail,
        analysis_status=row.analysis_status,  # type: ignore[arg-type]
        ai_summary=row.ai_summary,
        ai_audio=row.ai_audio,
        is_ai_thumbnail=row.is_ai_thumbnail,
        created_at=row.created_at or datetime.utcnow(),
    )


def _to_orm(domain: Video) -> dict:
    """Domain → ORM dict 변환 (upsert용)."""
    return {
        "title": domain.title,
        "category": domain.category,
        "description": domain.description,
        "url": domain.url,
        "owner_id": domain.owner_id,
        "thumbnail": domain.thumbnail,
        "analysis_status": domain.analysis_status,
        "ai_summary": domain.ai_summary,
        "ai_audio": domain.ai_audio,
        "is_ai_thumbnail": domain.is_ai_thumbnail,
    }


class SQLAlchemyVideoRepository(VideoRepository):
    """SQLAlchemy 기반 Video Repository."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_id(self, video_id: int) -> Video | None:
        row = self._db.query(VideoORM).filter(VideoORM.id == video_id).first()
        return _to_domain(row) if row else None

    def list_all(self, skip: int = 0, limit: int = 100) -> list[Video]:
        rows = self._db.query(VideoORM).offset(skip).limit(limit).all()
        return [_to_domain(r) for r in rows]

    def save(self, video: Video) -> Video:
        data = _to_orm(video)
        if video.id:
            row = self._db.query(VideoORM).filter(VideoORM.id == video.id).first()
            if row:
                for k, v in data.items():
                    setattr(row, k, v)
                self._db.commit()
                self._db.refresh(row)
                return _to_domain(row)
        # 신규 생성
        row = VideoORM(**data)
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return _to_domain(row)

    def delete(self, video_id: int) -> bool:
        row = self._db.query(VideoORM).filter(VideoORM.id == video_id).first()
        if not row:
            return False
        self._db.delete(row)
        self._db.commit()
        return True
