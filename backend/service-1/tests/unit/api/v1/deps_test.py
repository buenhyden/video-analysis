"""Unit tests for API dependency injection."""

from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from jose import jwt

from src.api.v1.deps import get_current_user
from src.core.config import settings
from src.models.user import User


@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    """Test successful user retrieval with valid JWT token."""
    mock_db = MagicMock()
    mock_user = User(id=1, username="testuser", hashed_password="hashed123")

    # Create a valid JWT token
    token_data = {"sub": "testuser"}
    valid_token = jwt.encode(token_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    # Mock get_user_by_username to return the user
    with patch("src.api.v1.deps.get_user_by_username", return_value=mock_user):
        result = await get_current_user(db=mock_db, token=valid_token)

        assert result.username == "testuser"
        assert result.id == 1


@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    """Test user retrieval with invalid JWT token."""
    mock_db = MagicMock()
    invalid_token = "invalid.jwt.token"

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(db=mock_db, token=invalid_token)

    assert exc_info.value.status_code == 403
    assert "Credentials validation failed" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_current_user_user_not_found():
    """Test user retrieval when user doesn't exist in database."""
    mock_db = MagicMock()

    # Create a valid JWT token
    token_data = {"sub": "nonexistent"}
    valid_token = jwt.encode(token_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    # Mock get_user_by_username to return None (user not found)
    with patch("src.api.v1.deps.get_user_by_username", return_value=None):
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(db=mock_db, token=valid_token)

        assert exc_info.value.status_code == 404
        assert "User not found" in exc_info.value.detail
