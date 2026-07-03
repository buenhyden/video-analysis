"""service-2: AnalysisTask Entity.

Video Analysis Bounded Context의 핵심 엔티티.
분석 파이프라인의 진행 상태를 캡슐화한다.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal

from src.domain.analysis.events import AnalysisCompleted

AnalysisStage = Literal["received", "frame_extraction", "description", "summary", "enrichment", "done", "failed"]


@dataclass
class AnalysisTask:
    """service-2 도메인 엔티티: 단일 비디오 분석 작업.

    Ubiquitous Language (service-2):
    - AnalysisTask: 비디오 한 건에 대한 분석 파이프라인 실행 단위
    - FrameExtraction: 키프레임 추출 단계
    - AISummary: VLM + LLM을 통한 요약 단계
    - AudioSynthesis: TTS를 통한 음성 생성 단계
    """

    video_id: int
    video_url: str
    trace_id: str | None = None
    stage: AnalysisStage = "received"
    frames: list[str] = field(default_factory=list)
    descriptions: list[str] = field(default_factory=list)
    ai_summary: str | None = None
    thumbnail_url: str | None = None
    audio_url: str | None = None
    error: str | None = None
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def mark_frame_extraction(self, frames: list[str]) -> None:
        """프레임 추출 완료."""
        if not frames:
            raise ValueError("service-2: FrameExtraction produced no frames")
        self.frames = frames
        self.stage = "frame_extraction"

    def mark_descriptions_generated(self, descriptions: list[str]) -> None:
        """이미지 설명 생성 완료."""
        if not descriptions:
            raise ValueError("service-2: No descriptions generated from frames")
        self.descriptions = descriptions
        self.stage = "description"

    def mark_summary_generated(self, summary: str) -> None:
        """AI 요약 완료."""
        if not summary:
            raise ValueError("service-2: Summary generation produced empty result")
        self.ai_summary = summary
        self.stage = "summary"

    def mark_enrichment_done(self, thumbnail_url: str | None, audio_url: str | None) -> None:
        """썸네일 + 오디오 생성 완료."""
        self.thumbnail_url = thumbnail_url
        self.audio_url = audio_url
        self.stage = "enrichment"

    def complete(self) -> AnalysisCompleted:
        """분석 성공 완료 이벤트 생성."""
        self.stage = "done"
        return AnalysisCompleted(
            video_id=self.video_id,
            status="completed",
            ai_summary=self.ai_summary,
            thumbnail_url=self.thumbnail_url,
            audio_url=self.audio_url,
        )

    def fail(self, reason: str) -> AnalysisCompleted:
        """분석 실패 이벤트 생성."""
        self.stage = "failed"
        self.error = reason
        return AnalysisCompleted(
            video_id=self.video_id,
            status="failed",
        )
