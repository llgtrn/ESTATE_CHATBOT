"""Tests for exceptions module."""
from app.core.exceptions import (
    BriefNotFoundError,
    CacheError,
    ChatbotException,
    ContentFilterError,
    DatabaseError,
    InvalidMessageError,
    LLMError,
    RateLimitError,
    SessionExpiredError,
    SessionNotFoundError,
    ValidationError,
)


class TestChatbotException:
    """Tests for ChatbotException class."""

    def test_basic_exception(self) -> None:
        """Test basic exception creation."""
        exc = ChatbotException(
            message="Test error",
            error_code="TEST_ERROR",
            status_code=400,
        )

        assert exc.message == "Test error"
        assert exc.error_code == "TEST_ERROR"
        assert exc.status_code == 400
        assert exc.details == {}
        assert str(exc) == "Test error"

    def test_exception_with_details(self) -> None:
        """Test exception with details."""
        details = {"field": "value", "count": 42}
        exc = ChatbotException(
            message="Test error",
            error_code="TEST_ERROR",
            details=details,
        )

        assert exc.details == details
        assert exc.details["field"] == "value"
        assert exc.details["count"] == 42

    def test_exception_default_status_code(self) -> None:
        """Test exception default status code."""
        exc = ChatbotException(
            message="Test error",
            error_code="TEST_ERROR",
        )

        assert exc.status_code == 500


class TestSessionNotFoundError:
    """Tests for SessionNotFoundError."""

    def test_session_not_found(self) -> None:
        """Test session not found error."""
        exc = SessionNotFoundError("session_123")

        assert "session_123" in exc.message
        assert exc.error_code == "SESSION_NOT_FOUND"
        assert exc.status_code == 404
        assert exc.details["session_id"] == "session_123"


class TestSessionExpiredError:
    """Tests for SessionExpiredError."""

    def test_session_expired(self) -> None:
        """Test session expired error."""
        exc = SessionExpiredError("session_456")

        assert "session_456" in exc.message
        assert exc.error_code == "SESSION_EXPIRED"
        assert exc.status_code == 410
        assert exc.details["session_id"] == "session_456"


class TestInvalidMessageError:
    """Tests for InvalidMessageError."""

    def test_invalid_message(self) -> None:
        """Test invalid message error."""
        exc = InvalidMessageError("Message is too short")

        assert exc.message == "Message is too short"
        assert exc.error_code == "INVALID_MESSAGE"
        assert exc.status_code == 400

    def test_invalid_message_with_details(self) -> None:
        """Test invalid message with details."""
        details = {"min_length": 1, "actual_length": 0}
        exc = InvalidMessageError("Message is too short", details)

        assert exc.details == details


class TestBriefNotFoundError:
    """Tests for BriefNotFoundError."""

    def test_brief_not_found(self) -> None:
        """Test brief not found error."""
        exc = BriefNotFoundError("brief_789")

        assert "brief_789" in exc.message
        assert exc.error_code == "BRIEF_NOT_FOUND"
        assert exc.status_code == 404
        assert exc.details["brief_id"] == "brief_789"


class TestValidationError:
    """Tests for ValidationError."""

    def test_validation_error(self) -> None:
        """Test validation error."""
        exc = ValidationError("Invalid budget value")

        assert exc.message == "Invalid budget value"
        assert exc.error_code == "VALIDATION_ERROR"
        assert exc.status_code == 422

    def test_validation_error_with_details(self) -> None:
        """Test validation error with details."""
        details = {"field": "budget", "error": "must be positive"}
        exc = ValidationError("Invalid budget value", details)

        assert exc.details == details


class TestLLMError:
    """Tests for LLMError."""

    def test_llm_error(self) -> None:
        """Test LLM error."""
        exc = LLMError("Model timeout")

        assert exc.message == "Model timeout"
        assert exc.error_code == "LLM_ERROR"
        assert exc.status_code == 500


class TestDatabaseError:
    """Tests for DatabaseError."""

    def test_database_error(self) -> None:
        """Test database error."""
        exc = DatabaseError("Connection failed")

        assert exc.message == "Connection failed"
        assert exc.error_code == "DATABASE_ERROR"
        assert exc.status_code == 500


class TestCacheError:
    """Tests for CacheError."""

    def test_cache_error(self) -> None:
        """Test cache error."""
        exc = CacheError("Redis connection failed")

        assert exc.message == "Redis connection failed"
        assert exc.error_code == "CACHE_ERROR"
        assert exc.status_code == 500


class TestContentFilterError:
    """Tests for ContentFilterError."""

    def test_content_filter_error(self) -> None:
        """Test content filter error."""
        exc = ContentFilterError("Inappropriate content detected")

        assert exc.message == "Inappropriate content detected"
        assert exc.error_code == "CONTENT_FILTER_ERROR"
        assert exc.status_code == 400


class TestRateLimitError:
    """Tests for RateLimitError."""

    def test_rate_limit_error(self) -> None:
        """Test rate limit error."""
        exc = RateLimitError()

        assert exc.message == "Rate limit exceeded"
        assert exc.error_code == "RATE_LIMIT_EXCEEDED"
        assert exc.status_code == 429

    def test_rate_limit_error_custom_message(self) -> None:
        """Test rate limit error with custom message."""
        exc = RateLimitError("Too many requests from this IP")

        assert exc.message == "Too many requests from this IP"
        assert exc.error_code == "RATE_LIMIT_EXCEEDED"
        assert exc.status_code == 429
