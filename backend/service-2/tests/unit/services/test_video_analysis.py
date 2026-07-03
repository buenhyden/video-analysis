"""Tests for src.services.video_analysis module."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.services.video_analysis import VideoAnalysisService

# Constants for test assertions
HTTP_STATUS_NOT_FOUND = 404
HTTP_STATUS_INTERNAL_ERROR = 500
MAX_KEYFRAMES_LIMIT = 15


class MockVideo:
    """Mock Video model for testing."""

    def __init__(self) -> None:
        """Initialize mock video with test data."""
        self.id = 1
        self.title = "Test Video"
        self.analysis_status = ""
        self.ai_summary = ""
        self.thumbnail = ""
        self.is_ai_thumbnail = False
        self.ai_audio = ""
        self.url = "http://video"


@pytest.fixture
def service():
    """Create VideoAnalysisService instance for testing."""
    return VideoAnalysisService(video_id=1)


def test_init(service):
    """Test VideoAnalysisService initialization."""
    assert service.video_id == 1


def test_get_db(service):
    """Test database session retrieval."""
    with patch("src.services.video_analysis.session_local_write") as mock_session:
        db = service._get_db()
        assert db == mock_session.return_value


def test_update_status_success(service):
    """Test successful status update."""
    mock_db = MagicMock()
    mock_video = MockVideo()
    query_filter = mock_db.query.return_value.filter.return_value
    query_filter.first.return_value = mock_video

    with patch.object(service, "_get_db", return_value=mock_db):
        title = service.update_status(
            "completed",
            summary="Summary",
            thumbnail_url="http://thumb",
            audio_url="http://audio",
        )

        assert title == "Test Video"
        assert mock_video.analysis_status == "completed"
        assert mock_video.ai_summary == "Summary"
        assert mock_video.thumbnail == "http://thumb"
        assert mock_video.ai_audio == "http://audio"
        mock_db.commit.assert_called_once()
        mock_db.close.assert_called_once()


def test_update_status_failure(service):
    """Test status update failure handling."""
    mock_db = MagicMock()
    mock_db.query.side_effect = Exception("DB Error")

    with patch.object(service, "_get_db", return_value=mock_db):
        title = service.update_status("failed")
        assert title == "Unknown Video"
        mock_db.rollback.assert_called_once()
        mock_db.close.assert_called_once()


@pytest.mark.asyncio
async def test_finalize_analysis(service):
    """Test finalize_analysis sends notification."""
    with (
        patch.object(service, "update_status", return_value="Title") as mock_update,
        patch("src.services.video_analysis.kafka_producer.send_message", new_callable=AsyncMock) as mock_kafka,
    ):
        await service.finalize_analysis("completed", summary="Summary")
        mock_update.assert_called_once_with("completed", "Summary", None, None)
        mock_kafka.assert_awaited_once()


def test_get_stream_url(service):
    """Test get_stream_url extracts URL from yt-dlp."""
    with patch("yt_dlp.YoutubeDL") as mock_ydl:
        mock_instance = mock_ydl.return_value.__enter__.return_value
        mock_instance.extract_info.return_value = {"url": "http://stream"}

        url = service.get_stream_url("http://youtube.com/v")
        assert url == "http://stream"


def test_get_stream_url_error(service):
    """Test get_stream_url returns None on error."""
    with patch("yt_dlp.YoutubeDL") as mock_ydl:
        mock_instance = mock_ydl.return_value.__enter__.return_value
        mock_instance.extract_info.side_effect = Exception("yt-dlp error")

        url = service.get_stream_url("http://youtube.com/v")
        assert url == "http://youtube.com/v"


def test_extract_keyframes(service):
    """Test extract_keyframes from YouTube video."""
    with patch("cv2.VideoCapture") as mock_cap:
        mock_instance = mock_cap.return_value
        mock_instance.get.return_value = 30  # fps
        mock_instance.isOpened.side_effect = [True, True, False]
        mock_instance.read.return_value = (True, MagicMock())

        with (
            patch("cv2.imencode", return_value=(True, b"buffer")),
            patch.object(service, "get_stream_url", return_value="http://stream"),
        ):
            frames = service.extract_keyframes("http://youtube.com/v", interval_sec=1)
            assert len(frames) > 0
            mock_instance.release.assert_called_once()


@pytest.mark.asyncio
async def test_generate_image_description(service):
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"response": "A description"}
        mock_post.return_value = mock_resp

        desc = await service.generate_image_description("base64data")
        assert desc == "A description"


@pytest.mark.asyncio
async def test_summarize_descriptions(service):
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"response": "A summary"}
        mock_post.return_value = mock_resp

        summary = await service.summarize_descriptions(["desc1", "desc2"])
        assert summary == "A summary"


@pytest.mark.asyncio
async def test_generate_thumbnail_prompt(service):
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"response": "Prompt text"}
        mock_post.return_value = mock_resp

        prompt = await service.generate_thumbnail_prompt("Summary")
        assert prompt == "Prompt text"


@pytest.mark.asyncio
async def test_generate_and_upload_thumbnail(service):
    with patch.object(service, "generate_thumbnail_prompt", return_value="Prompt"):
        with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.content = b"image data"
            mock_get.return_value = mock_resp

            with patch(
                "src.services.video_analysis.storage_client.upload_file", return_value="http://s3/thumb"
            ) as mock_upload:
                url = await service.generate_and_upload_thumbnail("Summary")
                assert url == "http://s3/thumb"
                mock_upload.assert_called_once()


@pytest.mark.asyncio
async def test_generate_and_upload_audio(service):
    # Mocking edge_tts is tricky, simplifies here
    with patch("edge_tts.Communicate") as mock_comm:
        mock_instance = mock_comm.return_value

        async def mock_stream() -> object:
            """Mock TTS stream generator."""
            yield {"type": "audio", "data": b"chunk"}

        mock_instance.stream.return_value = mock_stream()

        with patch("src.services.video_analysis.storage_client.upload_file", return_value="http://s3/audio"):
            url = await service.generate_and_upload_audio("Text")
            assert url == "http://s3/audio"


@pytest.mark.asyncio
async def test_process_video_success(service):
    with patch.object(service, "update_status"):
        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.scalar.return_value = "http://video"

        with patch.object(service, "_get_db", return_value=mock_db):
            with patch.object(service, "extract_keyframes", return_value=["frame"]):
                with patch.object(service, "generate_image_description", return_value="desc"):
                    with patch.object(service, "summarize_descriptions", return_value="summary"):
                        with patch.object(service, "generate_and_upload_thumbnail", return_value="t_url"):
                            with patch.object(service, "generate_and_upload_audio", return_value="a_url"):
                                with patch.object(service, "finalize_analysis", new_callable=AsyncMock) as mock_final:
                                    await service.process_video()
                                    mock_final.assert_awaited_once_with("completed", "summary", "t_url", "a_url")


@pytest.mark.asyncio
async def test_process_video_failed(service):
    with patch.object(service, "update_status"):
        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.scalar.return_value = None

        with patch.object(service, "_get_db", return_value=mock_db):
            with patch.object(service, "finalize_analysis", new_callable=AsyncMock) as mock_final:
                await service.process_video()
                mock_final.assert_awaited_once_with("failed")


@pytest.mark.asyncio
async def test_finalize_analysis_notification_failure(service):
    """Test finalize_analysis when notification fails."""
    mock_db = MagicMock()
    mock_video = MockVideo()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_video

    with patch.object(service, "_get_db", return_value=mock_db):
        # The code uses 'kafka_producer' instance imported from src.core.message_broker
        with patch("src.services.video_analysis.kafka_producer", new_callable=AsyncMock) as mock_kafka:
            mock_kafka.send_message.side_effect = Exception("Kafka down")

            # Should not raise exception
            await service.finalize_analysis("completed", "summary", "thumb", "audio")
            mock_kafka.send_message.assert_called_once()


def test_extract_keyframes_non_youtube(service):
    """Test extract_keyframes with a non-YouTube URL."""
    with patch("cv2.VideoCapture") as mock_cap_cls:
        mock_cap = mock_cap_cls.return_value
        mock_cap.isOpened.return_value = True
        import numpy as np

        frame = np.zeros((10, 10, 3), dtype=np.uint8)
        mock_cap.read.side_effect = [(True, frame), (False, None)]
        mock_cap.get.return_value = 0  # Triggers FPS fallback

        with patch("cv2.imencode", return_value=(True, b"frame")):
            frames = service.extract_keyframes("http://other.com/video.mp4")
            assert len(frames) > 0

        # Reset side effect for second call
        mock_cap.isOpened.side_effect = [True, True, False]
        mock_cap.read.side_effect = [(True, frame), (True, frame), (False, None)]
        # Ensure get_stream_url was NOT called
        with patch.object(service, "get_stream_url") as mock_get_stream:
            service.extract_keyframes("http://other.com/video.mp4")
            mock_get_stream.assert_not_called()


def test_extract_keyframes_limit(service):
    """Test extract_keyframes stops at 15 frames."""
    with patch("cv2.VideoCapture") as mock_cap_cls:
        mock_cap = mock_cap_cls.return_value
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (True, MagicMock())
        mock_cap.get.return_value = 30

        with patch("cv2.imencode", return_value=(True, b"frame")):
            # It will loop many times, but we want it to break at 15 frames
            # To avoid infinite loop in test, we should mock side_effect for read
            # but here it should hit the limit quickly.
            # Actually, the count % frame_interval will be 0 every frame if interval is 0?
            # No, count % frame_interval where count++
            frames = service.extract_keyframes("http://other.com/video.mp4", interval_sec=1)
            assert len(frames) == 15
