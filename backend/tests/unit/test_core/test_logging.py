"""Tests for logging module."""
import logging

from app.core.logging import StructuredFormatter, get_logger, setup_logging


class TestStructuredFormatter:
    """Tests for StructuredFormatter class."""

    def test_format(self) -> None:
        """Test JSON log formatting."""
        formatter = StructuredFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        formatted = formatter.format(record)

        assert "test" in formatted
        assert "INFO" in formatted
        assert "Test message" in formatted

    def test_format_with_exception(self) -> None:
        """Test formatting with exception."""
        formatter = StructuredFormatter()

        try:
            raise ValueError("Test error")
        except ValueError:
            import sys

            exc_info = sys.exc_info()

        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="test.py",
            lineno=10,
            msg="Error occurred",
            args=(),
            exc_info=exc_info,
        )

        formatted = formatter.format(record)

        assert "ERROR" in formatted
        assert "Error occurred" in formatted
        assert "ValueError" in formatted


class TestSetupLogging:
    """Tests for setup_logging function."""

    def test_setup_logging_info(self) -> None:
        """Test setting up logging with INFO level."""
        setup_logging("INFO")

        root_logger = logging.getLogger()
        assert root_logger.level == logging.INFO

    def test_setup_logging_debug(self) -> None:
        """Test setting up logging with DEBUG level."""
        setup_logging("DEBUG")

        root_logger = logging.getLogger()
        assert root_logger.level == logging.DEBUG

    def test_setup_logging_warning(self) -> None:
        """Test setting up logging with WARNING level."""
        setup_logging("WARNING")

        root_logger = logging.getLogger()
        assert root_logger.level == logging.WARNING


class TestGetLogger:
    """Tests for get_logger function."""

    def test_get_logger(self) -> None:
        """Test getting logger instance."""
        logger = get_logger("test_module")

        assert logger is not None
        assert logger.name == "test_module"

    def test_get_logger_different_names(self) -> None:
        """Test getting loggers with different names."""
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")

        assert logger1.name != logger2.name
