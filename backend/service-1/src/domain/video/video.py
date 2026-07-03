"""service-1: Video Aggregate Root.

Video Management Bounded Context의 핵심 애그리게이트.
비즈니스 불변식(invariant)을 캡슐화하고 상태 전환을 명시적으로 관리한다.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal

from src.domain.video.events import AnalysisCompleted, VideoQueued

AnalysisStatus = Literal["pending", "queued", "processing", "completed", "failed"]


@dataclass
class Video:
    """Video Aggregate Root.

    Ubiquitous Language (service-1):
    - Video: 사용자가 등록한 영상 콘텐츠
    - AnalysisStatus: 분석 파이프라인 상의 현재 상태
    - queued_for_analysis(): 분석 대기열에 등록하는 도메인 행동
    - complete_analysis(): 분석 결과를 적용하는 도메인 행동
    """

    id: int
    title: str
    category: str
    description: str
    url: str
    owner_id: int
    thumbnail: str | None = None
    analysis_status: AnalysisStatus = "pending"
    ai_summary: str | None = None
    ai_audio: str | None = None
    is_ai_thumbnail: bool | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def queued_for_analysis(self, requester: str, trace_id: str | None = None) -> VideoQueued:
        """분석 대기열에 등록한다.

        Invariant: 이미 처리 중이거나 큐에 있으면 재요청 불가.
        """
        if self.analysis_status in ("queued", "processing"):
            raise ValueError(
                f"Video {self.id} is already in '{self.analysis_status}' state. "
                "Cannot queue again."
            )
        self.analysis_status = "queued"
        return VideoQueued(
            video_id=self.id,
            video_url=self.url,
            requester=requester,
            trace_id=trace_id,
        )

    def complete_analysis(self, event: AnalysisCompleted) -> None:
        """분석 결과를 적용한다.

        Invariant: processing 상태여야만 완료 가능.
        """
        if self.analysis_status not in ("processing", "queued"):
            raise ValueError(
                f"Video {self.id} is in '{self.analysis_status}' state. "
                "Cannot apply analysis result."
            )
        self.analysis_status = event.status  # type: ignore[assignment]
        if event.ai_summary:
            self.ai_summary = event.ai_summary
        if event.thumbnail_url:
            self.thumbnail = event.thumbnail_url
            self.is_ai_thumbnail = True
        if event.audio_url:
            self.ai_audio = event.audio_url
