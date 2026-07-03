"""service-2: Thumbnail Generator Infrastructure Adapter.

Pollinations.ai API를 통해 AI 썸네일을 생성하고 MinIO에 업로드한다.
"""

import io
import logging
import urllib.parse
import uuid

import httpx

from src.core.storage import storage_client
from src.infrastructure.vlm.ollama_client import generate_thumbnail_prompt

logger = logging.getLogger(__name__)


async def generate_and_upload_thumbnail(video_id: int, summary: str) -> str | None:
    """AI 썸네일 생성 → MinIO 업로드 → URL 반환."""
    raw_prompt = await generate_thumbnail_prompt(summary)
    if not raw_prompt:
        return None

    clean_prompt = raw_prompt.replace("**", "").replace('"', "").replace("Movie Poster Thumbnail Prompt:", "").strip()
    encoded = urllib.parse.quote(f"cinematic shot, masterpiece, {clean_prompt}")

    try:
        async with httpx.AsyncClient(timeout=60.0, verify=False) as client:  # noqa: S501
            # Flux 모델 시도, 실패 시 Turbo fallback
            for model in ("flux", "turbo"):
                url = f"https://image.pollinations.ai/prompt/{encoded}?width=1280&height=720&model={model}&seed=42"
                resp = await client.get(url)
                if resp.status_code == httpx.codes.OK:
                    image_data = io.BytesIO(resp.content)
                    filename = f"ai_thumb_{video_id}_{uuid.uuid4().hex[:8]}.jpg"
                    result = storage_client.upload_file(image_data, object_name=filename)
                    logger.info("service-2: Thumbnail uploaded for video %s", video_id)
                    return result
                logger.warning("service-2: Thumbnail model '%s' failed (%s)", model, resp.status_code)
    except Exception as e:
        logger.error("service-2: Thumbnail generation failed: %s", e)

    return None
