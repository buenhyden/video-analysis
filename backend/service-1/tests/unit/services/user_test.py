"""Unit tests for user service functions."""

from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session

from src.models.user import User
from src.schemas.user import UserCreate
from src.services.user.create_user import create_user
from src.services.user.get_user_by_username import get_user_by_username


def test_create_user_success():
    """Test successful user creation."""
    # Mock DB Session
    mock_db = MagicMock(spec=Session)

    # Mock UserCreate data
    user_in = UserCreate(username="testuser", password="password123")

    # Mock get_password_hash
    with patch("src.services.user.create_user.get_password_hash", return_value="hashed_secret"):
        # Call the function
        result = create_user(mock_db, user_in)

        # Assertions
        assert result.username == "testuser"
        assert result.hashed_password == "hashed_secret"

        # Verify DB interactions
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()


# --- Get User by Username Tests ---


def test_get_user_by_username_found():
    """Test successful user retrieval by username."""
    mock_db = MagicMock(spec=Session)
    mock_user = User(id=1, username="testuser", hashed_password="hashed123")

    # Mock query chain
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = mock_user
    mock_db.query.return_value = mock_query

    result = get_user_by_username(mock_db, username="testuser")

    assert result is not None
    assert result.username == "testuser"
    assert result.id == 1


def test_get_user_by_username_not_found():
    """Test user retrieval when user doesn't exist."""
    mock_db = MagicMock(spec=Session)

    # Mock query to return None (user not found)
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = None
    mock_db.query.return_value = mock_query

    result = get_user_by_username(mock_db, username="nonexistent")

    assert result is None
