"""service-1: QueueVideoAnalysis Use Case.

이미 존재하는 비디오를 재분석 대기열에 등록한다.
"""

import logging

from src.domain.video.video import Video
from src.domain.video.video_repository import VideoRepository
from src.domain.video.events import VideoQueued

logger = logging.getLogger(__name__)


class QueueVideoAnalysisUseCase:
    """기존 Video를 분석 대기열에 재등록한다."""

    def __init__(self, repo: VideoRepository) -> None:
        self._repo = repo

    def execute(
        self,
        video_id: int,
        requester: str,
        trace_id: str | None = None,
    ) -> tuple[Video, VideoQueued]:
        """
        Raises:
            ValueError: 비디오를 찾을 수 없거나 잘못된 상태인 경우.
        Returns:
            (Video, VideoQueued) - 업데이트된 비디오와 Kafka 발행용 이벤트.
        """
        video = self._repo.get_by_id(video_id)
        if not video:
            raise ValueError(f"service-1: Video {video_id} not found")

        # 도메인 행동 → 불변식 검사 + 상태 전환
        event = video.queued_for_analysis(requester=requester, trace_id=trace_id)
        self._repo.save(video)

        logger.info("service-1: Video %s re-queued for analysis by %s", video_id, requester)
        return video, event
