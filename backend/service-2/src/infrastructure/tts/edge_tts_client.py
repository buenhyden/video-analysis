"""service-2: TTS (Text-to-Speech) Infrastructure Adapter.

Edge TTS를 통해 AI 요약 텍스트를 한국어 음성으로 변환하고 MinIO에 업로드한다.
"""

import io
import logging
import uuid

import edge_tts

from src.core.storage import storage_client

logger = logging.getLogger(__name__)

TTS_VOICE = "ko-KR-SunHiNeural"


async def synthesize_and_upload_audio(video_id: int, text: str) -> str | None:
    """텍스트 → MP3 음성 변환 → MinIO 업로드 → URL 반환."""
    if not text:
        return None
    try:
        communicate = edge_tts.Communicate(text, TTS_VOICE)
        audio_buffer = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_buffer.write(chunk["data"])
        audio_buffer.seek(0)

        filename = f"ai_audio_{video_id}_{uuid.uuid4().hex[:8]}.mp3"
        url = storage_client.upload_file(audio_buffer, object_name=filename, content_type="audio/mpeg")
        logger.info("service-2: Audio synthesized and uploaded for video %s", video_id)
        return url
    except Exception as e:
        logger.error("service-2: TTS synthesis failed for video %s: %s", video_id, e)
        return None
