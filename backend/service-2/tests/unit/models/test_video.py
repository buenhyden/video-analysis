"""Comprehensive tests for models.video module."""

from src.models.video import Video


def test_video_module_imports():
    """Test that video module can be imported."""
    from src.models import video

    assert video is not None


def test_video_class_exists():
    """Test Video class exists."""
    assert Video is not None


def test_video_tablename():
    """Test Video has correct tablename."""
    assert Video.__tablename__ == "videos"


def test_video_has_id_column():
    """Test Video has id column."""
    assert hasattr(Video, "id")


def test_video_has_title_column():
    """Test Video has title column."""
    assert hasattr(Video, "title")


def test_video_has_owner_id_column():
    """Test Video has owner_id column."""
    assert hasattr(Video, "owner_id")


def test_video_has_created_at_column():
    """Test Video has created_at column."""
    assert hasattr(Video, "created_at")


def test_video_has_analysis_status_column():
    """Test Video has analysis_status column."""
    assert hasattr(Video, "analysis_status")


def test_video_has_ai_summary_column():
    """Test Video has ai_summary column."""
    assert hasattr(Video, "ai_summary")


def test_video_has_thumbnail_column():
    """Test Video has thumbnail column."""
    assert hasattr(Video, "thumbnail")


def test_video_has_is_ai_thumbnail_column():
    """Test Video has is_ai_thumbnail column."""
    assert hasattr(Video, "is_ai_thumbnail")


def test_video_has_ai_audio_column():
    """Test Video has ai_audio column."""
    assert hasattr(Video, "ai_audio")


def test_video_has_owner_relationship():
    """Test Video has owner relationship."""
    assert hasattr(Video, "owner")


def test_video_class_name():
    """Test Video class name."""
    assert Video.__name__ == "Video"
