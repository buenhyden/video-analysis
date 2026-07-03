"""Comprehensive tests for core.config.settings module."""

from src.core.config import settings


def test_settings_module_imports():
    """Test that settings module can be imported."""
    assert settings is not None


def test_settings_has_project_name():
    """Test settings has PROJECT_NAME."""
    assert hasattr(settings, "PROJECT_NAME")
    assert settings.PROJECT_NAME is not None


def test_settings_has_database_urls():
    """Test settings has database URLs."""
    assert hasattr(settings, "SQLALCHEMY_DATABASE_WRITE_URL")
    assert hasattr(settings, "SQLALCHEMY_DATABASE_READ_URL")


def test_settings_has_kafka_config():
    """Test settings has Kafka configuration."""
    assert hasattr(settings, "KAFKA_BROKERS")
    assert hasattr(settings, "KAFKA_TOPIC_ANALYSIS")
    assert hasattr(settings, "KAFKA_GROUP_ID")


def test_settings_has_redis_url():
    """Test settings has Redis URL."""
    assert hasattr(settings, "REDIS_URL")
    assert settings.REDIS_URL is not None


def test_settings_has_aws_config():
    """Test settings has AWS/MinIO configuration."""
    assert hasattr(settings, "AWS_ACCESS_KEY_ID")
    assert hasattr(settings, "AWS_SECRET_ACCESS_KEY")
    assert hasattr(settings, "AWS_REGION")
    assert hasattr(settings, "AWS_ENDPOINT_URL")
    assert hasattr(settings, "AWS_BUCKET_NAME")


def test_settings_has_cors_origins():
    """Test settings has CORS origins."""
    assert hasattr(settings, "CORS_ORIGINS")


def test_settings_has_default_port():
    """Test settings has DEFAULT_PORT."""
    assert hasattr(settings, "DEFAULT_PORT")
    assert isinstance(settings.DEFAULT_PORT, int)


def test_settings_has_secret_key():
    """Test settings has SECRET_KEY."""
    assert hasattr(settings, "SECRET_KEY")
    assert settings.SECRET_KEY is not None


def test_settings_has_algorithm():
    """Test settings has ALGORITHM."""
    assert hasattr(settings, "ALGORITHM")
    assert settings.ALGORITHM == "HS256"


def test_settings_kafka_brokers_is_list():
    """Test KAFKA_BROKERS is a list."""
    assert isinstance(settings.KAFKA_BROKERS, list)


def test_settings_cors_origins_is_list_or_str():
    """Test CORS_ORIGINS is list or str."""
    assert isinstance(settings.CORS_ORIGINS, (list, str))
