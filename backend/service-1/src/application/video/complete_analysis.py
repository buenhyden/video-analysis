"""service-1: CompleteAnalysis Use Case (Anti-Corruption Layer).

service-2의 Kafka 이벤트를 service-1 도메인 언어로 변환하여 적용한다.
이 유스케이스가 두 Bounded Context 간의 Anti-Corruption Layer 역할을 한다.
"""

import logging

from src.domain.video.video_repository import VideoRepository
from src.domain.video.events import AnalysisCompleted

logger = logging.getLogger(__name__)


class CompleteAnalysisUseCase:
    """service-2의 분석 완료 이벤트를 수신하여 Video 상태를 업데이트한다."""

    def __init__(self, repo: VideoRepository) -> None:
        self._repo = repo

    def execute(self, event: AnalysisCompleted) -> bool:
        """
        Args:
            event: service-2로부터 수신한 AnalysisCompleted 이벤트.
        Returns:
            True if updated, False if video not found.
        """
        video = self._repo.get_by_id(event.video_id)
        if not video:
            logger.warning("service-1: Video %s not found for analysis completion", event.video_id)
            return False

        try:
            video.complete_analysis(event)
            self._repo.save(video)
            logger.info(
                "service-1: Video %s analysis %s applied (summary=%s)",
                event.video_id,
                event.status,
                bool(event.ai_summary),
            )
            return True
        except ValueError as e:
            logger.error("service-1: Cannot apply analysis result - %s", e)
            return False
