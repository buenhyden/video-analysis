"""service-1: CreateVideo Use Case.

Video Management Bounded Context의 비디오 생성 유스케이스.
썸네일 자동 추출 로직을 포함하며 VideoQueued 도메인 이벤트를 반환한다.
"""

import logging
import re

from src.domain.video.video import Video
from src.domain.video.video_repository import VideoRepository
from src.domain.video.events import VideoQueued

logger = logging.getLogger(__name__)

DEFAULT_THUMBNAIL = "https://placehold.co/800x450/1e293b/cbd5e1.png?text=No+Thumbnail"


def _extract_youtube_thumbnail(url: str) -> str | None:
    """YouTube URL에서 썸네일 URL을 추출한다."""
    pattern = (
        r"(?:https?://)?(?:www\.)?"
        r"(?:youtube\.com/(?:[^/\n\s]+/\S+/|(?:v|e(?:mbed)?)/|\S*?[?&]v=)|youtu\.be/)"
        r"([a-zA-Z0-9_-]{11})"
    )
    match = re.search(pattern, url)
    if match:
        return f"https://img.youtube.com/vi/{match.group(1)}/maxresdefault.jpg"
    return None


class CreateVideoUseCase:
    """비디오를 생성하고 분석 대기열에 등록한다."""

    def __init__(self, repo: VideoRepository) -> None:
        self._repo = repo

    def execute(
        self,
        title: str,
        category: str,
        description: str,
        url: str,
        owner_id: int,
        thumbnail: str | None,
        requester: str,
        trace_id: str | None = None,
    ) -> tuple[Video, VideoQueued]:
        """
        Returns:
            (Video, VideoQueued) - 저장된 비디오와 Kafka 발행용 이벤트.
        """
        resolved_thumbnail = thumbnail or _extract_youtube_thumbnail(url) or DEFAULT_THUMBNAIL

        # 새 Video 도메인 객체 (id=0은 아직 미저장 상태)
        video = Video(
            id=0,
            title=title,
            category=category,
            description=description,
            url=url,
            owner_id=owner_id,
            thumbnail=resolved_thumbnail,
        )
        # 도메인 행동 → 상태 전환 + 이벤트 생성
        event = video.queued_for_analysis(requester=requester, trace_id=trace_id)

        # 영속성 저장
        saved = self._repo.save(video)
        # 저장된 id를 이벤트에 반영
        final_event = VideoQueued(
            video_id=saved.id,
            video_url=saved.url,
            requester=event.requester,
            trace_id=event.trace_id,
        )
        logger.info("service-1: Video %s created and queued by %s", saved.id, requester)
        return saved, final_event
