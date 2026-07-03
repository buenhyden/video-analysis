"""Unit tests for video service functions."""

from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.models.video import Video
from src.schemas.video import VideoCreate
from src.services.video.create_video import create_video
from src.services.video.delete_video import delete_video
from src.services.video.extract_thumbnail import extract_thumbnail


def test_create_video_success():
    """Test successful video creation."""
    # Mock DB Session
    mock_db = MagicMock(spec=Session)

    # Mock VideoCreate data
    video_in = VideoCreate(
        title="Test Video",
        description="Test Description",
        url="http://example.com/video.mp4",
        category="Test Category",
    )
    user_id = 1

    # Mock extract_thumbnail to return a dummy URL
    with patch(
        "src.services.video.create_video.extract_thumbnail",
        return_value="http://example.com/thumb.jpg",
    ):
        # Call the function
        result = create_video(mock_db, video_in, user_id)

        # Assertions
        assert result.title == "Test Video"
        assert result.owner_id == user_id
        assert result.thumbnail == "http://example.com/thumb.jpg"

        # Verify DB interactions
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()


def test_create_video_auto_thumbnail_failure():
    """Test video creation when thumbnail extraction fails."""
    # Mock DB Session
    mock_db = MagicMock(spec=Session)

    # Mock VideoCreate data without thumbnail
    video_in = VideoCreate(
        title="Test Video",
        description="Test Description",
        url="http://example.com/video.mp4",
        category="Test Category",
    )
    user_id = 1

    # Mock extract_thumbnail to return None (failure)
    with patch("src.services.video.create_video.extract_thumbnail", return_value=None):
        # Call the function
        result = create_video(mock_db, video_in, user_id)

        # Assertions
        assert result.thumbnail == "https://placehold.co/800x450/1e293b/cbd5e1.png?text=No+Thumbnail"

        # Verify DB interactions
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()


# --- Delete Video Tests ---


def test_delete_video_success():
    """Test successful video deletion."""
    mock_db = MagicMock(spec=Session)
    mock_video = Video(id=1, title="Test Video", url="http://example.com")

    # Mock query chain
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = mock_video
    mock_db.query.return_value = mock_query

    result = delete_video(mock_db, video_id=1)

    assert result is True
    mock_db.delete.assert_called_once_with(mock_video)
    mock_db.commit.assert_called_once()


def test_delete_video_not_found():
    """Test video deletion when video doesn't exist."""
    mock_db = MagicMock(spec=Session)

    # Mock query to return None (video not found)
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = None
    mock_db.query.return_value = mock_query

    result = delete_video(mock_db, video_id=999)

    assert result is False
    mock_db.delete.assert_not_called()
    mock_db.commit.assert_not_called()


def test_delete_video_database_error():
    """Test video deletion when database error occurs."""
    mock_db = MagicMock(spec=Session)
    mock_video = Video(id=1, title="Test Video", url="http://example.com")

    # Mock query chain
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = mock_video
    mock_db.query.return_value = mock_query

    # Simulate database error on delete
    mock_db.delete.side_effect = SQLAlchemyError("Database error")

    with pytest.raises(SQLAlchemyError):
        delete_video(mock_db, video_id=1)

    mock_db.rollback.assert_called_once()


# --- Extract Thumbnail Tests ---


def test_extract_thumbnail_youtube_watch():
    """Test thumbnail extraction from YouTube watch URL."""
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    result = extract_thumbnail(url)
    assert result == "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"


def test_extract_thumbnail_youtube_short():
    """Test thumbnail extraction from YouTube short URL."""
    url = "https://youtu.be/dQw4w9WgXcQ"
    result = extract_thumbnail(url)
    assert result == "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"


def test_extract_thumbnail_youtube_embed():
    """Test thumbnail extraction from YouTube embed URL."""
    url = "https://www.youtube.com/embed/dQw4w9WgXcQ"
    result = extract_thumbnail(url)
    assert result == "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"


def test_extract_thumbnail_invalid_url():
    """Test thumbnail extraction from non-YouTube URL."""
    url = "https://example.com/video.mp4"
    result = extract_thumbnail(url)
    assert result is None


def test_extract_thumbnail_empty_url():
    """Test thumbnail extraction from empty URL."""
    result = extract_thumbnail("")
    assert result is None
