"""Video Thumbnail Extraction Module."""

import logging
import re

logger = logging.getLogger(__name__)


def extract_thumbnail(url: str) -> str | None:
    """비디오 URL에서 썸네일 이미지를 자동으로 추출합니다.

    현재는 YouTube URL만 지원합니다.
    """
    if not url:
        return None

    # YouTube Video ID 추출 정규식
    # 지원 형식: youtube.com/watch?v=ID, youtu.be/ID, youtube.com/embed/ID 등
    youtube_regex = (
        r"(?:https?:\/\/)?(?:www\.)?"
        r"(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)"
        r"([a-zA-Z0-9_-]{11})"
    )

    match = re.search(youtube_regex, url)
    if match:
        video_id = match.group(1)
        # 고해상도 썸네일 URL 반환
        return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

    return None
