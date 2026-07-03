"""Tests for core.message_broker.product_client module."""

from unittest.mock import AsyncMock, patch

import pytest

from src.core.message_broker.product_client import KafkaProducerClient


@pytest.fixture(autouse=True)
def reset_singleton():
    """Reset the singleton instance before each test."""
    KafkaProducerClient._instance = None


class TestKafkaProducerClient:
    """Test KafkaProducerClient singleton and methods."""

    def test_singleton(self):
        """Test singleton pattern."""
        client1 = KafkaProducerClient()
        client2 = KafkaProducerClient()
        assert client1 is client2

    @pytest.mark.asyncio
    async def test_start_stop(self):
        """Test start and stop methods."""
        with patch("src.core.message_broker.product_client.AIOKafkaProducer") as mock_producer_cls:
            mock_producer = mock_producer_cls.return_value
            mock_producer.start = AsyncMock()
            mock_producer.stop = AsyncMock()

            client = KafkaProducerClient()
            await client.start()
            assert client.producer is not None
            mock_producer.start.assert_awaited_once()

            await client.stop()
            mock_producer.stop.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_send_message_success(self):
        """Test send_message success."""
        with patch("src.core.message_broker.product_client.AIOKafkaProducer") as mock_producer_cls:
            mock_producer = mock_producer_cls.return_value
            mock_producer.send_and_wait = AsyncMock()

            client = KafkaProducerClient()
            client.producer = mock_producer

            await client.send_message("test-topic", {"key": "value"})
            mock_producer.send_and_wait.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_send_message_no_producer(self):
        """Test send_message with no producer initialized."""
        client = KafkaProducerClient()
        client.producer = None

        # Should just log a warning and return
        await client.send_message("topic", {})

    @pytest.mark.asyncio
    async def test_send_message_failure(self):
        """Test send_message failure."""
        with patch("src.core.message_broker.product_client.AIOKafkaProducer") as mock_producer_cls:
            mock_producer = mock_producer_cls.return_value
            mock_producer.send_and_wait = AsyncMock(side_effect=Exception("Kafka error"))

            client = KafkaProducerClient()
            client.producer = mock_producer

            with pytest.raises(Exception):
                await client.send_message("topic", {})
