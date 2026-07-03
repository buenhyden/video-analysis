from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.api.v1 import deps
from src.core.database import get_read_db, get_write_db
from src.main import app
from src.schemas.user import User
from src.schemas.video import Video


@pytest.fixture
def client():
    # Mock DB connection in lifespan
    with (
        patch("src.main.Base.metadata.create_all"),
        patch("src.main.session_local_write"),
        patch("src.main.get_user_by_username"),
        patch("src.main.create_user"),
        # Mock Kafka and Cache start/stop in lifespan
        patch("src.main.kafka_producer.start", new_callable=AsyncMock),
        patch("src.main.kafka_producer.stop", new_callable=AsyncMock),
        patch("src.main.cache_client.start", new_callable=AsyncMock),
        patch("src.main.cache_client.stop", new_callable=AsyncMock),
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


def override_get_current_user():
    return User(id=1, username="testuser", is_active=True)


app.dependency_overrides[get_read_db] = override_get_db
app.dependency_overrides[get_write_db] = override_get_db
app.dependency_overrides[deps.get_current_user] = override_get_current_user


def test_read_videos(client):
    # Mock get_videos service and cache_client
    with (
        patch("src.api.v1.videos.get_videos") as mock_get_videos,
        patch("src.api.v1.videos.cache_client") as mock_cache,
    ):
        # Mock cache miss (AsyncMock)
        mock_cache.get = AsyncMock(return_value=None)
        mock_cache.set = AsyncMock()

        mock_get_videos.return_value = [
            Video(
                id=1,
                title="Video 1",
                description="Desc 1",
                url="http://v1.com",
                owner_id=1,
                thumbnail="http://t1.com",
                category="Cat 1",
                created_at=datetime(2023, 1, 1),
                analysis_status="pending",
            ),
            Video(
                id=2,
                title="Video 2",
                description="Desc 2",
                url="http://v2.com",
                owner_id=1,
                thumbnail="http://t2.com",
                category="Cat 2",
                created_at=datetime(2023, 1, 1),
                analysis_status="completed",
            ),
        ]

        response = client.get("/api/v1/videos/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Video 1"


def test_create_video_api(client):
    # Mock create_video service, kafka_producer, and cache_client
    with (
        patch("src.api.v1.videos.crud_create_video") as mock_create_video,
        patch("src.api.v1.videos.kafka_producer") as mock_kafka,
        patch("src.api.v1.videos.cache_client") as mock_cache,
    ):
        # Configure AsyncMocks
        mock_kafka.send_message = AsyncMock()
        mock_cache.delete_pattern = AsyncMock()

        mock_create_video.return_value = Video(
            id=1,
            title="New Video",
            description="New Desc",
            url="http://new.com",
            owner_id=1,
            thumbnail="http://thumb.com",
            category="New Cat",
            created_at=datetime(2023, 1, 1),
            analysis_status="pending",
        )

        payload = {
            "title": "New Video",
            "description": "New Desc",
            "url": "http://new.com",
            "category": "New Cat",
        }
        response = client.post("/api/v1/videos/", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Video"
        assert data["id"] == 1


def test_delete_video_api(client):
    # Mock delete_video service and cache_client
    with (
        patch("src.api.v1.videos.crud_delete_video") as mock_delete_video,
        patch("src.api.v1.videos.cache_client") as mock_cache,
    ):
        # Configure AsyncMock
        mock_cache.delete_pattern = AsyncMock()

        mock_delete_video.return_value = True

        response = client.delete("/api/v1/videos/1")
        assert response.status_code == 200
        assert response.json() == {"status": "success"}


def test_delete_video_not_found(client):
    # Mock delete_video service to return False
    with patch("src.api.v1.videos.crud_delete_video") as mock_delete_video:
        mock_delete_video.return_value = False

        response = client.delete("/api/v1/videos/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Video not found"
