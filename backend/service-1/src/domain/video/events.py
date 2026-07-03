"""service-1: Video Management Domain Events."""

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class VideoQueued:
    """비디오 분석 큐 등록 이벤트."""

    video_id: int
    video_url: str
    requester: str
    trace_id: str | None = None
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class AnalysisCompleted:
    """분석 완료 이벤트 (service-2로부터 수신)."""

    video_id: int
    status: str  # "completed" | "failed"
    ai_summary: str | None = None
    thumbnail_url: str | None = None
    audio_url: str | None = None
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
