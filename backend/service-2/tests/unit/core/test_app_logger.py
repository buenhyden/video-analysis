"""Comprehensive tests for core.logger.app_logger module."""

from src.core.logger.app_logger import AppLogger


def test_app_logger_module_imports():
    """Test that app_logger module can be imported."""
    from src.core.logger import app_logger

    assert app_logger is not None


def test_app_logger_class_exists():
    """Test AppLogger class exists."""
    assert AppLogger is not None


def test_app_logger_has_setup_method():
    """Test AppLogger has setup method."""
    logger = AppLogger()
    assert hasattr(logger, "setup")
    assert callable(logger.setup)


def test_app_logger_can_instantiate():
    """Test AppLogger can be instantiated."""
    logger = AppLogger()
    assert logger is not None


def test_app_logger_setup_returns_logger():
    """Test setup method returns a logger."""
    app_logger = AppLogger()
    logger = app_logger.setup(service_name="test", enable_console=False, enable_file=False, enable_loki=False)
    assert logger is not None


def test_app_logger_has_trace_id_filter_class():
    """Test AppLogger has _TraceIdFilter inner class."""
    assert hasattr(AppLogger, "_TraceIdFilter")


def test_app_logger_can_create_multiple_instances():
    """Test multiple AppLogger instances can be created."""
    logger1 = AppLogger()
    logger2 = AppLogger()
    assert logger1 is not None
    assert logger2 is not None
