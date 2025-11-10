"""Tests for configuration module."""
import logging

import pytest
from pydantic import ValidationError

from app.config import Settings, get_settings


class TestSettings:
    """Tests for Settings class."""

    def test_default_settings(self) -> None:
        """Test default settings."""
        settings = Settings()

        assert settings.app_name == "Real Estate Chatbot"
        assert settings.app_version == "1.0.0"
        assert settings.environment == "dev"
        assert not settings.debug
        assert settings.log_level == "INFO"

    def test_custom_settings(self) -> None:
        """Test custom settings."""
        settings = Settings(
            environment="production",
            debug=True,
            log_level="DEBUG",
        )

        assert settings.environment == "production"
        assert settings.debug
        assert settings.log_level == "DEBUG"

    def test_invalid_log_level(self) -> None:
        """Test invalid log level."""
        with pytest.raises(ValidationError):
            Settings(log_level="INVALID")

    def test_valid_log_levels(self) -> None:
        """Test valid log levels."""
        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            settings = Settings(log_level=level)
            assert settings.log_level == level

    def test_log_level_case_insensitive(self) -> None:
        """Test log level is case insensitive."""
        settings = Settings(log_level="debug")
        assert settings.log_level == "DEBUG"

    def test_is_production(self) -> None:
        """Test is_production property."""
        settings = Settings(environment="production")
        assert settings.is_production

        settings = Settings(environment="dev")
        assert not settings.is_production

    def test_is_development(self) -> None:
        """Test is_development property."""
        settings = Settings(environment="dev")
        assert settings.is_development

        settings = Settings(environment="production")
        assert not settings.is_development

    def test_database_url(self) -> None:
        """Test database URL."""
        settings = Settings()
        assert "postgresql+asyncpg://" in str(settings.database_url)

    def test_redis_url(self) -> None:
        """Test Redis URL."""
        settings = Settings()
        assert "redis://" in str(settings.redis_url)

    def test_api_settings(self) -> None:
        """Test API settings."""
        settings = Settings()
        assert settings.api_v1_prefix == "/api/v1"
        assert isinstance(settings.allowed_origins, list)
        assert settings.max_request_size == 10485760
        assert settings.rate_limit_per_minute == 100

    def test_database_settings(self) -> None:
        """Test database settings."""
        settings = Settings()
        assert settings.database_pool_size == 20
        assert settings.database_max_overflow == 10
        assert not settings.database_echo

    def test_redis_settings(self) -> None:
        """Test Redis settings."""
        settings = Settings()
        assert settings.redis_max_connections == 50
        assert settings.redis_ttl_seconds == 3600

    def test_gcp_settings(self) -> None:
        """Test GCP settings."""
        settings = Settings(
            gcp_project_id="test-project",
            gcp_region="asia-northeast1",
        )
        assert settings.gcp_project_id == "test-project"
        assert settings.gcp_region == "asia-northeast1"

    def test_llm_settings(self) -> None:
        """Test LLM settings."""
        settings = Settings()
        assert settings.gemini_flash_model == "gemini-1.5-flash-002"
        assert settings.gemini_pro_model == "gemini-1.5-pro-002"
        assert settings.gemini_temperature == 0.7
        assert settings.gemini_max_tokens == 2048

    def test_embedding_settings(self) -> None:
        """Test embedding settings."""
        settings = Settings()
        assert settings.embedding_model == "text-embedding-004"
        assert settings.embedding_dimensions == 768

    def test_session_settings(self) -> None:
        """Test session settings."""
        settings = Settings()
        assert settings.session_max_turns == 50
        assert settings.session_timeout_minutes == 60
        assert settings.session_max_tokens == 100000

    def test_safety_settings(self) -> None:
        """Test safety settings."""
        settings = Settings()
        assert settings.enable_content_filter
        assert settings.enable_pii_masking
        assert settings.max_retries == 3

    def test_monitoring_settings(self) -> None:
        """Test monitoring settings."""
        settings = Settings()
        assert settings.enable_metrics
        assert settings.enable_tracing
        assert settings.metrics_port == 9090

    def test_configure_logging(self) -> None:
        """Test logging configuration."""
        settings = Settings(log_level="WARNING")
        settings.configure_logging()

        root_logger = logging.getLogger()
        assert root_logger.level == logging.WARNING

    def test_get_settings_cached(self) -> None:
        """Test get_settings returns cached instance."""
        settings1 = get_settings()
        settings2 = get_settings()

        assert settings1 is settings2
