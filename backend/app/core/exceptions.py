"""Custom exceptions for the chatbot application."""
from typing import Any


class ChatbotException(Exception):
    """Base exception for all chatbot errors."""

    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = 500,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize exception."""
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class SessionNotFoundError(ChatbotException):
    """Session not found."""

    def __init__(self, session_id: str) -> None:
        """Initialize exception."""
        super().__init__(
            message=f"Session {session_id} not found",
            error_code="SESSION_NOT_FOUND",
            status_code=404,
            details={"session_id": session_id},
        )


class SessionExpiredError(ChatbotException):
    """Session has expired."""

    def __init__(self, session_id: str) -> None:
        """Initialize exception."""
        super().__init__(
            message=f"Session {session_id} has expired",
            error_code="SESSION_EXPIRED",
            status_code=410,
            details={"session_id": session_id},
        )


class InvalidMessageError(ChatbotException):
    """Invalid message format or content."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        """Initialize exception."""
        super().__init__(
            message=message,
            error_code="INVALID_MESSAGE",
            status_code=400,
            details=details or {},
        )


class BriefNotFoundError(ChatbotException):
    """Brief not found."""

    def __init__(self, brief_id: str) -> None:
        """Initialize exception."""
        super().__init__(
            message=f"Brief {brief_id} not found",
            error_code="BRIEF_NOT_FOUND",
            status_code=404,
            details={"brief_id": brief_id},
        )


class ValidationError(ChatbotException):
    """Validation error."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        """Initialize exception."""
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=422,
            details=details or {},
        )


class LLMError(ChatbotException):
    """LLM processing error."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        """Initialize exception."""
        super().__init__(
            message=message,
            error_code="LLM_ERROR",
            status_code=500,
            details=details or {},
        )


class DatabaseError(ChatbotException):
    """Database operation error."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        """Initialize exception."""
        super().__init__(
            message=message,
            error_code="DATABASE_ERROR",
            status_code=500,
            details=details or {},
        )


class CacheError(ChatbotException):
    """Cache operation error."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        """Initialize exception."""
        super().__init__(
            message=message,
            error_code="CACHE_ERROR",
            status_code=500,
            details=details or {},
        )


class ContentFilterError(ChatbotException):
    """Content filtering error."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        """Initialize exception."""
        super().__init__(
            message=message,
            error_code="CONTENT_FILTER_ERROR",
            status_code=400,
            details=details or {},
        )


class RateLimitError(ChatbotException):
    """Rate limit exceeded."""

    def __init__(self, message: str = "Rate limit exceeded") -> None:
        """Initialize exception."""
        super().__init__(
            message=message,
            error_code="RATE_LIMIT_EXCEEDED",
            status_code=429,
        )
