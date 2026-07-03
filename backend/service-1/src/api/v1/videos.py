"""service-1: Video API Router (Presentation Layer).

Application Use Case에 위임하며, Domain 객체를 직접 노출하지 않는다.
"""

import logging
import json
from typing import Annotated, Any

from asgi_correlation_id import correlation_id
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from src.api.v1 import deps
from src.application.video.create_video import CreateVideoUseCase
from src.application.video.queue_video_analysis import QueueVideoAnalysisUseCase
from src.core.cache import cache_client
from src.core.config import settings
from src.core.database import get_read_db, get_write_db
from src.core.message_broker import kafka_producer
from src.core.storage import storage_client
from src.infrastructure.repositories.sqlalchemy_video_repository import SQLAlchemyVideoRepository
from src.infrastructure.orm.video_orm import VideoORM
from src.schemas import User, Video, VideoCreate

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/", response_model=list[Video])  # type: ignore[misc]
async def read_videos(
    db: Annotated[Session, Depends(get_read_db)],
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """비디오 목록 조회 (캐싱 적용)."""
    cache_key = f"videos:list:{skip}:{limit}"
    cached = await cache_client.get(cache_key)
    if cached:
        logger.info("service-1: Cache HIT for %s", cache_key)
        return cached

    repo = SQLAlchemyVideoRepository(db)
    videos = repo.list_all(skip=skip, limit=limit)
    if videos:
        video_dicts = [
            json.loads(Video.model_validate(v, from_attributes=True).model_dump_json())
            for v in videos
        ]
        await cache_client.set(cache_key, video_dicts, ttl=60)
    logger.info("service-1: Fetched %s videos from DB", len(videos))
    return videos


@router.post("/", response_model=Video)  # type: ignore[misc]
async def create_video(
    *,
    video_in: VideoCreate,
    db: Annotated[Session, Depends(get_write_db)],
    current_user: Annotated[User, Depends(deps.get_current_user)],
) -> Any:
    """비디오 생성 및 분석 자동 큐 등록."""
    logger.info("service-1: User %s creating video '%s'", current_user.username, video_in.title)
    try:
        repo = SQLAlchemyVideoRepository(db)
        use_case = CreateVideoUseCase(repo)
        saved, event = use_case.execute(
            title=video_in.title,
            category=video_in.category,
            description=video_in.description,
            url=video_in.url,
            owner_id=current_user.id,
            thumbnail=video_in.thumbnail,
            requester=current_user.username,
            trace_id=correlation_id.get(),
        )
        # Kafka 이벤트 발행 (VideoQueued)
        await kafka_producer.send_message(
            settings.KAFKA_TOPIC_ANALYSIS,
            {
                "video_id": event.video_id,
                "url": event.video_url,
                "trace_id": event.trace_id,
                "requester": event.requester,
            },
        )
        await cache_client.delete_pattern("videos:list:*")
        return saved
    except Exception as e:
        logger.error("service-1: Error creating video: %s", e)
        raise HTTPException(status_code=500, detail="Could not create video") from e


@router.post("/{video_id}/analyze", response_model=dict)  # type: ignore[misc]
async def analyze_video(
    video_id: int,
    db: Annotated[Session, Depends(get_write_db)],
    current_user: Annotated[User, Depends(deps.get_current_user)],
) -> Any:
    """비디오 재분석 요청."""
    logger.info("service-1: User %s re-queueing video %s", current_user.username, video_id)
    try:
        repo = SQLAlchemyVideoRepository(db)
        use_case = QueueVideoAnalysisUseCase(repo)
        _, event = use_case.execute(
            video_id=video_id,
            requester=current_user.username,
            trace_id=correlation_id.get(),
        )
        await kafka_producer.send_message(
            settings.KAFKA_TOPIC_ANALYSIS,
            {
                "video_id": event.video_id,
                "url": event.video_url,
                "trace_id": event.trace_id,
                "requester": event.requester,
            },
        )
        await cache_client.delete_pattern("videos:list:*")
        return {"message": "Analysis request queued", "status": "queued"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Could not queue analysis") from e


@router.delete("/{video_id}")  # type: ignore[misc]
async def delete_video(
    video_id: int,
    db: Annotated[Session, Depends(get_write_db)],
    current_user: Annotated[User, Depends(deps.get_current_user)],
) -> Any:
    """비디오 삭제."""
    repo = SQLAlchemyVideoRepository(db)
    deleted = repo.delete(video_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Video not found")
    await cache_client.delete_pattern("videos:list:*")
    return {"status": "success"}


@router.patch("/{video_id}/thumbnail", response_model=Video)  # type: ignore[misc]
async def upload_manual_thumbnail(
    video_id: int,
    file: Annotated[UploadFile, File(...)],
    db: Annotated[Session, Depends(get_write_db)],
    current_user: Annotated[User, Depends(deps.get_current_user)],
) -> Any:
    """수동 썸네일 업로드."""
    import uuid

    repo = SQLAlchemyVideoRepository(db)
    video = repo.get_by_id(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    if video.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    filename = f"user_thumb_{video_id}_{uuid.uuid4().hex[:8]}.jpg"
    s3_url = storage_client.upload_file(file.file, object_name=filename, content_type=file.content_type)
    if not s3_url:
        raise HTTPException(status_code=500, detail="Failed to upload thumbnail")

    video.thumbnail = s3_url
    video.is_ai_thumbnail = False
    repo.save(video)
    await cache_client.delete_pattern("videos:list:*")
    return video
