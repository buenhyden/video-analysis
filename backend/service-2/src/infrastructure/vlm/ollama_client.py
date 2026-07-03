"""service-2: VLM (Vision Language Model) Client Adapter.

Ollama를 통한 이미지 설명 생성 및 텍스트 요약을 담당한다.
모델 설정은 core/config에서 주입된다.
"""

import logging

import httpx

from src.core.config import settings

logger = logging.getLogger(__name__)

VLM_MODEL = "minicpm-v:8b"
LLM_MODEL = "exaone3.5:7.8b"
TIMEOUT = 120.0


async def generate_image_description(base64_image: str) -> str:
    """VLM을 사용하여 단일 이미지 설명을 생성한다."""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT, verify=False) as client:  # noqa: S501
            resp = await client.post(
                f"{settings.OLLAMA_URL}/api/generate",
                json={
                    "model": VLM_MODEL,
                    "prompt": "Describe this image in detail.",
                    "images": [base64_image],
                    "stream": False,
                },
            )
            if resp.status_code == httpx.codes.OK:
                return str(resp.json().get("response", ""))
            logger.error("service-2: VLM error %s", resp.status_code)
            return ""
    except Exception as e:
        logger.error("service-2: VLM connection error: %s", e)
        return ""


async def summarize_descriptions(descriptions: list[str]) -> str:
    """여러 장면 설명을 하나의 한국어 요약으로 통합한다."""
    if not descriptions:
        return ""
    full_text = "\n".join(f"Scene {i + 1}: {d}" for i, d in enumerate(descriptions))
    prompt = (
        f"Here are descriptions of scenes from a video:\n{full_text}\n\n"
        "Based on these descriptions, please summarize the overall content of the video in Korean."
    )
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT, verify=False) as client:  # noqa: S501
            resp = await client.post(
                f"{settings.OLLAMA_URL}/api/generate",
                json={"model": LLM_MODEL, "prompt": prompt, "stream": False},
            )
            if resp.status_code == httpx.codes.OK:
                return str(resp.json().get("response", ""))
            return ""
    except Exception as e:
        logger.error("service-2: LLM connection error: %s", e)
        return ""


async def generate_thumbnail_prompt(summary: str) -> str:
    """요약을 기반으로 영문 이미지 생성 프롬프트를 생성한다."""
    instruction = (
        f"Based on the summary below, write a high-quality text-to-image prompt "
        f"for a movie poster style thumbnail. Write ONLY the English prompt.\n\nSummary: {summary}"
    )
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT, verify=False) as client:  # noqa: S501
            resp = await client.post(
                f"{settings.OLLAMA_URL}/api/generate",
                json={"model": LLM_MODEL, "prompt": instruction, "stream": False, "options": {"temperature": 0.7}},
            )
            if resp.status_code == httpx.codes.OK:
                return resp.json().get("response", "").strip()
            return ""
    except Exception as e:
        logger.error("service-2: Prompt gen error: %s", e)
        return ""
