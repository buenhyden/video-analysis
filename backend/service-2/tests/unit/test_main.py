"""Tests for src.main module."""

import json
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.main import consume


class MockConsumer:
    """Mock Kafka Consumer for testing."""

    def __init__(self, messages: list[Any]) -> None:
        """Initialize mock consumer with messages."""
        self.messages = messages
        self.start = AsyncMock()
        self.stop = AsyncMock()

    def __aiter__(self) -> "MockConsumer":
        """Return async iterator."""
        return self

    async def __anext__(self) -> object:
        """Return next message or raise StopAsyncIteration."""
        if not self.messages:
            raise StopAsyncIteration
        return self.messages.pop(0)


@pytest.mark.asyncio
async def test_consume_loop():
    """Test the consume loop in main.py."""
    with patch("src.main.AIOKafkaConsumer", autospec=True) as mock_consumer_cls:
        # Create a real-ish mock consumer
        mock_msg = MagicMock()
        mock_msg.value = json.dumps({"video_id": 123, "trace_id": "abc"}).encode("utf-8")
        mock_consumer = MockConsumer([mock_msg])
        mock_consumer_cls.return_value = mock_consumer

        with patch("src.main.VideoAnalysisService", autospec=True) as mock_service_cls:
            mock_service = mock_service_cls.return_value
            mock_service.process_video = AsyncMock()

            # The consume() function will loop over mock_consumer once
            await consume()

            mock_consumer.start.assert_awaited_once()
            mock_service_cls.assert_called_once()
            mock_service.process_video.assert_awaited_once()
            mock_consumer.stop.assert_awaited_once()


@pytest.mark.asyncio
async def test_consume_exception():
    """Test exception handling in the consume loop."""
    with patch("src.main.AIOKafkaConsumer", autospec=True) as mock_consumer_cls:
        mock_msg = MagicMock()
        mock_msg.value = b'{"video_id": 123}'
        mock_consumer = MockConsumer([mock_msg])
        mock_consumer_cls.return_value = mock_consumer

        with patch("src.main.VideoAnalysisService", autospec=True) as mock_service_cls:
            mock_service = mock_service_cls.return_value
            mock_service.process_video.side_effect = Exception("Analysis failed")

            # The exception should be caught by the inner try-except
            await consume()

            mock_consumer.stop.assert_awaited_once()
