"""Comprehensive tests for models.user module."""

from src.models.user import User


def test_user_module_imports():
    """Test that user module can be imported."""
    from src.models import user

    assert user is not None


def test_user_class_exists():
    """Test User class exists."""
    assert User is not None


def test_user_tablename():
    """Test User has correct tablename."""
    assert User.__tablename__ == "users"


def test_user_has_id_column():
    """Test User has id column."""
    assert hasattr(User, "id")


def test_user_has_username_column():
    """Test User has username column."""
    assert hasattr(User, "username")


def test_user_has_hashed_password_column():
    """Test User has hashed_password column."""
    assert hasattr(User, "hashed_password")


def test_user_has_is_active_column():
    """Test User has is_active column."""
    assert hasattr(User, "is_active")


def test_user_has_videos_relationship():
    """Test User has videos relationship."""
    assert hasattr(User, "videos")


def test_user_class_name():
    """Test User class name."""
    assert User.__name__ == "User"
