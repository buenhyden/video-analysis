"""Comprehensive tests for core.cache.cache_client module."""

from src.core.cache.cache_client import CacheClient


def test_cache_client_module_imports():
    """Test that cache_client module can be imported."""
    from src.core.cache import cache_client

    assert cache_client is not None


def test_cache_client_class_exists():
    """Test CacheClient class exists."""
    assert CacheClient is not None


def test_cache_client_singleton():
    """Test CacheClient follows singleton pattern."""
    client1 = CacheClient()
    client2 = CacheClient()

    assert client1 is client2


def test_cache_client_has_start_method():
    """Test CacheClient has start method."""
    client = CacheClient()
    assert hasattr(client, "start")
    assert callable(client.start)


def test_cache_client_has_stop_method():
    """Test CacheClient has stop method."""
    client = CacheClient()
    assert hasattr(client, "stop")
    assert callable(client.stop)


def test_cache_client_has_get_method():
    """Test CacheClient has get method."""
    client = CacheClient()
    assert hasattr(client, "get")
    assert callable(client.get)


def test_cache_client_has_set_method():
    """Test CacheClient has set method."""
    client = CacheClient()
    assert hasattr(client, "set")
    assert callable(client.set)


def test_cache_client_has_delete_pattern_method():
    """Test CacheClient has delete_pattern method."""
    client = CacheClient()
    assert hasattr(client, "delete_pattern")
    assert callable(client.delete_pattern)


def test_cache_client_has_redis_client_attribute():
    """Test CacheClient has redis_client attribute."""
    client = CacheClient()
    assert hasattr(client, "redis_client")


def test_cache_client_new_returns_same_instance():
    """Test __new__ returns same instance."""
    CacheClient._instance = None  # Reset for test
    client1 = CacheClient()
    client2 = CacheClient()
    CacheClient._instance = None  # Reset after test

    assert client1 is client2
