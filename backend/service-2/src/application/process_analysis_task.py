"""service-2: ProcessAnalysisTask Use Case.

Video Analysis Bounded Context의 핵심 유스케이스.
AnalysisTask 도메인 엔티티를 사용하여 파이프라인을 조율하고,
각 인프라 어댑터에 위임한다.
"""

import asyncio
import logging

from src.domain.analysis.analysis_task import AnalysisTask
from src.domain.analysis.events import AnalysisCompleted
from src.infrastructure.video.frame_extractor import extract_keyframes
from src.infrastructure.vlm.ollama_client import generate_image_description, summarize_descriptions
from src.infrastructure.thumbnail.thumbnail_generator import generate_and_upload_thumbnail
from src.infrastructure.tts.edge_tts_client import synthesize_and_upload_audio

logger = logging.getLogger(__name__)


class ProcessAnalysisTaskUseCase:
    """비디오 분석 파이프라인을 실행한다.

    Stages (AnalysisTask 엔티티의 stage 필드로 추적):
      1. FrameExtraction
      2. ImageDescription (VLM)
      3. Summarization (LLM)
      4. Enrichment (Thumbnail + Audio, 병렬)
    """

    async def execute(self, video_id: int, video_url: str) -> AnalysisCompleted:
        """
        Returns:
            AnalysisCompleted 도메인 이벤트 (성공 또는 실패).
        """
        task = AnalysisTask(video_id=video_id, video_url=video_url)
        logger.info("service-2: Starting AnalysisTask for video %s", video_id)

        try:
            # Stage 1: 프레임 추출
            frames = extract_keyframes(video_url)
            task.mark_frame_extraction(frames)

            # Stage 2: 이미지 설명 생성 (VLM)
            descriptions = []
            for frame in task.frames:
                desc = await generate_image_description(frame)
                if desc:
                    descriptions.append(desc)
            task.mark_descriptions_generated(descriptions)

            # Stage 3: AI 요약 (LLM)
            summary = await summarize_descriptions(task.descriptions)
            task.mark_summary_generated(summary)

            # Stage 4: 썸네일 + 오디오 병렬 생성
            thumbnail_url, audio_url = await asyncio.gather(
                generate_and_upload_thumbnail(video_id, task.ai_summary),  # type: ignore[arg-type]
                synthesize_and_upload_audio(video_id, task.ai_summary),  # type: ignore[arg-type]
            )
            task.mark_enrichment_done(thumbnail_url, audio_url)

            completed_event = task.complete()
            logger.info("service-2: AnalysisTask completed for video %s", video_id)
            return completed_event

        except Exception as e:
            logger.error("service-2: AnalysisTask failed for video %s: %s", video_id, e)
            return task.fail(str(e))
