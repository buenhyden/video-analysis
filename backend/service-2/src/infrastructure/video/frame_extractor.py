"""service-2: Frame Extractor Infrastructure Adapter.

yt-dlp + OpenCV를 사용하여 비디오에서 키프레임을 추출한다.
Domain 계층에 외부 라이브러리 의존성이 침투하지 않도록 격리한다.
"""

import base64
import logging

import cv2
import yt_dlp

logger = logging.getLogger(__name__)

MAX_FRAMES = 15
DEFAULT_FPS_FALLBACK = 30


def _get_stream_url(youtube_url: str) -> str:
    """YouTube URL에서 실제 스트리밍 URL 추출."""
    ydl_opts = {
        "format": "best[ext=mp4]",
        "quiet": True,
        "extractor_args": {
            "youtube": {"player_client": ["android", "web"]}
        },
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            return info["url"]  # type: ignore[no-any-return]
    except Exception as e:
        logger.error("service-2: yt-dlp failed for %s: %s", youtube_url, e)
        return youtube_url


def extract_keyframes(video_url: str, interval_sec: int = 5) -> list[str]:
    """비디오에서 키프레임을 Base64 문자열 리스트로 추출한다."""
    if "youtube.com" in video_url or "youtu.be" in video_url:
        target_url = _get_stream_url(video_url)
    else:
        target_url = video_url

    frames: list[str] = []
    try:
        cap = cv2.VideoCapture(target_url)
        fps = cap.get(cv2.CAP_PROP_FPS) or DEFAULT_FPS_FALLBACK
        frame_interval = int(fps * interval_sec)
        count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if count % frame_interval == 0:
                _, buffer = cv2.imencode(".jpg", frame)
                frames.append(base64.b64encode(buffer).decode("utf-8"))
                if len(frames) >= MAX_FRAMES:
                    break
            count += 1
        cap.release()
    except Exception as e:
        logger.error("service-2: Frame extraction error: %s", e)
        raise

    logger.info("service-2: Extracted %d frames from %s", len(frames), video_url[:60])
    return frames
