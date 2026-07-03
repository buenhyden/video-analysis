"""Unit tests for cache client."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.core.cache.cache_client import CacheClient


@pytest.mark.asyncio
async def test_cache_client_singleton():
    """Test that CacheClient is a singleton."""
    client1 = CacheClient()
    client2 = CacheClient()

    assert client1 is client2


@pytest.mark.asyncio
async def test_cache_get_set():
    """Test cache set and get operations."""
    client = CacheClient()
    mock_redis = AsyncMock()

    # Mock redis client
    client.redis_client = mock_redis
    mock_redis.setex = AsyncMock()
    mock_redis.get = AsyncMock(return_value='{"key": "value"}')

    # Test set operation
    await client.set("test_key", {"key": "value"}, ttl=300)
    mock_redis.setex.assert_called_once()

    # Test get operation
    result = await client.get("test_key")
    assert result == {"key": "value"}
    mock_redis.get.assert_called_once_with("test_key")


@pytest.mark.asyncio
async def test_cache_delete_pattern():
    """Test cache deletion by pattern."""
    client = CacheClient()
    mock_redis = AsyncMock()

    # Mock redis client
    client.redis_client = mock_redis

    # Mock scan_iter to return some keys
    async def async_gen() -> AsyncMock:  # type: ignore[misc]
        yield "key1"
        yield "key2"

    mock_redis.scan_iter = MagicMock(return_value=async_gen())
    mock_redis.delete = AsyncMock()

    # Test delete by pattern
    await client.delete_pattern("test:*")

    mock_redis.delete.assert_called_once()


@pytest.mark.asyncio
async def test_cache_get_no_connection():
    """Test cache get when Redis is not connected."""
    client = CacheClient()
    client.redis_client = None

    result = await client.get("test_key")
    assert result is None


@pytest.mark.asyncio
async def test_cache_set_no_connection():
    """Test cache set when Redis is not connected."""
    client = CacheClient()
    client.redis_client = None

    # Should not raise an exception, just return silently
    await client.set("test_key", "value")


@pytest.mark.asyncio
async def test_cache_connection_start():
    """Test cache client startup and connection."""
    client = CacheClient()

    with patch("src.core.cache.cache_client.RedisCluster") as mock_redis_cluster:
        mock_redis = AsyncMock()
        mock_redis.ping = AsyncMock()
        mock_redis_cluster.from_url.return_value = mock_redis

        await client.start()

        assert client.redis_client is not None
        mock_redis.ping.assert_called_once()
