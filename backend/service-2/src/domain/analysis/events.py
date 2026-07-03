"""service-2: Video Analysis Domain Events."""

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class AnalysisTaskReceived:
    """분석 작업 수신 이벤트 (service-1 → service-2)."""

    video_id: int
    video_url: str
    trace_id: str | None = None
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class AnalysisCompleted:
    """분석 완료 이벤트 (service-2 발행 → service-1 수신)."""

    video_id: int
    status: str  # "completed" | "failed" | "processing"
    ai_summary: str | None = None
    thumbnail_url: str | None = None
    audio_url: str | None = None
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
