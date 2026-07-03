"""Video Analysis Service module."""

import asyncio
import base64
import io
import logging
import urllib.parse
import uuid

import cv2
import edge_tts
import httpx

# 분리된 모듈 import
import requests
import yt_dlp
from sqlalchemy.orm import Session

from src.core.config import settings
from src.core.message_broker import kafka_producer
from src.core.storage import storage_client

logger = logging.getLogger("worker.analysis")


class VideoAnalysisService:
    """Service for analyzing videos securely."""

    def __init__(self, video_id: int, video_url: str | None = None) -> None:
        """Initialize VideoAnalysisService."""
        self.video_id = video_id
        self.video_url = video_url

    async def finalize_analysis(
        self,
        status: str,
        summary: str | None = None,
        thumbnail_url: str | None = None,
        audio_url: str | None = None,
    ) -> None:
        """분석 결과를 마무리하고 알림을 전송합니다."""
        try:
            notification_message = {
                "event": f"analysis_{status}",
                "video_id": self.video_id,
                "status": status,
                "ai_summary": summary,
                "thumbnail_url": thumbnail_url,
                "audio_url": audio_url,
            }

            topic = getattr(settings, "KAFKA_TOPIC_NOTIFICATION", "video-notifications")
            await kafka_producer.send_message(topic, notification_message)
            logger.info(f"Sent notification event for Video {self.video_id} (Status: {status})")
        except Exception as e:
            logger.error(f"Failed to send notification event: {e}")

    def get_stream_url(self, youtube_url: str) -> str:
        """YouTube URL에서 실제 스트리밍 URL을 추출합니다."""
        # [수정] JS 런타임 오류 방지를 위한 extractor_args 추가
        ydl_opts = {
            "format": "best[ext=mp4]",
            "quiet": True,
            "extractor_args": {
                "youtube": {
                    "player_client": ["android", "web"]  # 모바일 클라이언트 흉내로 JS 우회 시도
                }
            },
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=False)
                return info["url"]  # type: ignore[no-any-return]
        except Exception as e:
            logger.error(f"yt-dlp failed: {e}")
            return youtube_url

    def extract_keyframes(self, video_url: str, interval_sec: int = 5) -> list[str]:
        """비디오에서 키프레임을 추출하여 Base64 문자열 리스트로 반환합니다."""
        frames = []
        try:
            if "youtube.com" in video_url or "youtu.be" in video_url:
                target_url = self.get_stream_url(video_url)
            else:
                target_url = video_url

            cap = cv2.VideoCapture(target_url)
            fps = cap.get(cv2.CAP_PROP_FPS)
            if fps == 0:
                fps = 30  # Fallback
            frame_interval = int(fps * interval_sec)
            count = 0

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                if count % frame_interval == 0:
                    _, buffer = cv2.imencode(".jpg", frame)
                    b64_image = base64.b64encode(buffer).decode("utf-8")
                    frames.append(b64_image)
                    if len(frames) >= 15:  # noqa: PLR2004
                        break
                count += 1
            cap.release()
            return frames
        except Exception as e:
            logger.error(f"Frame extraction error: {e}")
            raise e

    async def generate_image_description(self, base64_image: str) -> str:
        """VLM을 사용하여 이미지에 대한 설명을 생성합니다."""
        prompt = "Describe this image in detail."
        try:
            async with httpx.AsyncClient(timeout=120.0, verify=False) as client:  # noqa: S501
                resp = await client.post(
                    f"{settings.OLLAMA_URL}/api/generate",
                    json={
                        "model": "minicpm-v:8b",
                        "prompt": prompt,
                        "images": [base64_image],
                        "stream": False,
                    },
                )
                if resp.status_code == httpx.codes.OK:
                    return str(resp.json().get("response", ""))
                else:
                    logger.error(f"VLM Error: {resp.text}")
                    return "Description failed."
                return ""
        except Exception as e:
            logger.error(f"VLM Connection Error: {e}")
            return ""

    async def summarize_descriptions(self, descriptions: list[str]) -> str:
        """여러 이미지 설명들을 하나의 비디오 요약으로 통합합니다."""
        if not descriptions:
            return "No descriptions available to summarize."
        full_text = "\n".join([f"Scene {i + 1}: {desc}" for i, desc in enumerate(descriptions)])
        prompt = (
            f"Here are descriptions of scenes from a video:\n{full_text}\n\n"
            "Based on these descriptions, please summarize the overall content of the video in Korean."
        )

        try:
            async with httpx.AsyncClient(timeout=120.0, verify=False) as client:  # noqa: S501
                resp = await client.post(
                    f"{settings.OLLAMA_URL}/api/generate",
                    json={"model": "exaone3.5:7.8b", "prompt": prompt, "stream": False},
                )
                if resp.status_code == httpx.codes.OK:
                    return str(resp.json().get("response", ""))
                else:
                    return "Summary generation failed."
        except Exception as e:
            logger.error(f"LLM Connection Error: {e}")
            return "Summary generation failed."

    async def generate_thumbnail_prompt(self, summary: str) -> str:
        """이미지 생성을 위한 영문 프롬프트 요청."""
        try:
            prompt_instruction = (
                f"Based on the summary below, write a high-quality text-to-image prompt "
                f"for a movie poster style thumbnail. Write ONLY the English prompt.\n\nSummary: {summary}"
            )
            async with httpx.AsyncClient(timeout=120.0, verify=False) as client:  # noqa: S501
                resp = await client.post(
                    f"{settings.OLLAMA_URL}/api/generate",
                    json={
                        "model": "exaone3.5:7.8b",
                        "prompt": prompt_instruction,
                        "stream": False,
                        "options": {"temperature": 0.7},
                    },
                )
                return resp.json().get("response", "").strip() if resp.status_code == requests.codes.ok else ""
        except Exception as e:
            logger.error(f"Prompt gen error: {e}")
            return ""

    async def generate_and_upload_thumbnail(self, summary: str) -> str | None:
        """이미지 생성 -> 다운로드 -> MinIO 업로드 -> URL 반환."""
        # 1. 프롬프트 생성
        raw_prompt = await self.generate_thumbnail_prompt(summary)
        if not raw_prompt:
            return None

        clean_prompt = (
            raw_prompt.replace("**", "").replace('"', "").replace("Movie Poster Thumbnail Prompt:", "").strip()
        )

        try:
            encoded_prompt = urllib.parse.quote(f"cinematic shot, masterpiece, {clean_prompt}")

            # [수정] 모델 Fallback 로직 추가
            # 1. Flux 모델 시도
            image_url = (
                f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&model=flux&seed=42"
            )

            async with httpx.AsyncClient(timeout=60.0, verify=False) as client:  # noqa: S501
                resp = await client.get(image_url)

                if resp.status_code != httpx.codes.OK:
                    return None
                image_data = io.BytesIO(resp.content)  # 파일 객체로 변환

                # Flux 실패 시 Turbo 모델로 재시도
                if resp.status_code != requests.codes.ok:
                    logger.error(f"Flux model failed ({resp.status_code}). Retrying with Turbo model...")
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&model=turbo&seed=42"
                    resp = await client.get(image_url)

                if resp.status_code != requests.codes.ok:
                    logger.error(f"Image generation failed finally: {resp.text}")
                    return None

                image_data = io.BytesIO(resp.content)

            filename = f"ai_thumb_{self.video_id}_{uuid.uuid4().hex[:8]}.jpg"
            return storage_client.upload_file(image_data, object_name=filename)

        except Exception as e:
            logger.error(f"Thumbnail generation/upload failed: {e}")
            return None

    async def generate_and_upload_audio(self, text: str) -> str | None:
        """텍스트를 음성(MP3)으로 변환하여 MinIO에 업로드합니다."""
        if not text:
            return None

        try:
            communicate = edge_tts.Communicate(text, "ko-KR-SunHiNeural")
            audio_buffer = io.BytesIO()
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_buffer.write(chunk["data"])
            audio_buffer.seek(0)

            filename = f"ai_audio_{self.video_id}_{uuid.uuid4().hex[:8]}.mp3"
            s3_url = storage_client.upload_file(audio_buffer, object_name=filename, content_type="audio/mpeg")
            logger.info(f"TTS Audio generated in memory: {s3_url}")
            return s3_url
        except Exception as e:
            logger.error(f"TTS generation/upload failed: {e}")
            return None

    async def process_video(self) -> None:
        """비디오 분석 프로세스를 실행합니다."""
        # 1. 상태 업데이트 알림
        await self.finalize_analysis("processing")
        logger.info(f"Starting analysis for Video {self.video_id}")

        if not self.video_url:
            logger.error("No video_url provided")
            await self.finalize_analysis("failed")
            return

        try:
            # 1. 프레임 추출
            frames = self.extract_keyframes(self.video_url)
            if not frames:
                raise Exception("No frames extracted")

            # 2. 이미지 설명 생성
            descs = []
            for frame in frames:
                d = await self.generate_image_description(frame)
                if d:
                    descs.append(d)

            # 설명 생성 실패 시 조기 실패 처리
            if not descs:
                raise Exception("Failed to generate image descriptions")

            # 3. 요약 생성
            summary = await self.summarize_descriptions(descs)

            if not summary or summary == "Failed":
                raise Exception("Summary generation failed")

            # 4. 썸네일 & 오디오 생성 (병렬)
            ai_thumb_task = self.generate_and_upload_thumbnail(summary)
            ai_audio_task = self.generate_and_upload_audio(summary)
            results = await asyncio.gather(ai_thumb_task, ai_audio_task)
            thumbnail_url, audio_url = results

            # 5. 최종 완료 처리
            await self.finalize_analysis("completed", summary, thumbnail_url, audio_url)

        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            await self.finalize_analysis("failed")
