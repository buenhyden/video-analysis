from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.core.database import get_write_db
from src.main import app


@pytest.fixture
def client():
    # Mock DB connection in lifespan
    with (
        patch("src.main.Base.metadata.create_all"),
        patch("src.main.session_local_write"),
        patch("src.main.get_user_by_username"),
        patch("src.main.create_user"),
        TestClient(app) as c,
    ):
        yield c


# Mock dependencies
def override_get_db():
    try:
        db = MagicMock()
        yield db
    finally:
        pass


app.dependency_overrides[get_write_db] = override_get_db


def test_login_success(client):
    # Mock get_user_by_username
    # Mock get_user_by_username
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.username = "testuser"
    mock_user.hashed_password = "hashed_password"
    mock_user.email = "test@example.com"
    mock_user.is_active = True

    with (
        patch("src.api.v1.auth.get_user_by_username", return_value=mock_user),
        patch("src.api.v1.auth.verify_password", return_value=True),
        patch("src.api.v1.auth.create_access_token", return_value="access_token_123"),
    ):
        response = client.post("/api/v1/auth/login", data={"username": "testuser", "password": "password"})

        assert response.status_code == 200
        data = response.json()
        assert data["access_token"] == "access_token_123"
        assert data["token_type"] == "bearer"


def test_login_failure_invalid_credentials(client):
    # Mock get_user_by_username to return None or verify_password to return False
    with patch("src.api.v1.auth.get_user_by_username", return_value=None):
        response = client.post("/api/v1/auth/login", data={"username": "wronguser", "password": "password"})
        assert response.status_code == 400
        assert response.json()["detail"] == "Incorrect username or password"
