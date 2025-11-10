"""Application configuration using Pydantic Settings."""
import logging
from functools import lru_cache
from typing import Literal

from pydantic import Field, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "Real Estate Chatbot"
    app_version: str = "1.0.0"
    environment: Literal["dev", "staging", "production"] = "dev"
    debug: bool = Field(default=False, description="Enable debug mode")
    log_level: str = Field(default="INFO", description="Logging level")

    # API
    api_v1_prefix: str = "/api/v1"
    allowed_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        description="CORS allowed origins",
    )
    max_request_size: int = Field(default=10485760, description="Max request size (10MB)")
    rate_limit_per_minute: int = Field(default=100, description="Rate limit per IP")

    # Database
    database_url: PostgresDsn = Field(
        default="postgresql+asyncpg://chatbot:password@localhost:5432/chatbot",
        description="PostgreSQL connection URL",
    )
    database_pool_size: int = Field(default=20, description="Database connection pool size")
    database_max_overflow: int = Field(default=10, description="Max overflow connections")
    database_echo: bool = Field(default=False, description="Echo SQL queries")

    # Redis
    redis_url: RedisDsn = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL",
    )
    redis_max_connections: int = Field(default=50, description="Max Redis connections")
    redis_ttl_seconds: int = Field(default=3600, description="Default TTL (1 hour)")

    # Google Cloud
    gcp_project_id: str = Field(default="", description="GCP Project ID")
    gcp_region: str = Field(default="asia-northeast1", description="GCP Region")
    gcp_location: str = Field(default="asia-northeast1", description="Vertex AI location")

    # LangChain / LLM
    langsmith_api_key: str = Field(default="", description="LangSmith API key")
    langsmith_project: str = Field(default="real-estate-chatbot", description="LangSmith project")
    langsmith_tracing: bool = Field(default=False, description="Enable LangSmith tracing")

    gemini_flash_model: str = Field(
        default="gemini-1.5-flash-002",
        description="Gemini Flash model name",
    )
    gemini_pro_model: str = Field(
        default="gemini-1.5-pro-002",
        description="Gemini Pro model name",
    )
    gemini_temperature: float = Field(default=0.7, description="LLM temperature")
    gemini_max_tokens: int = Field(default=2048, description="Max output tokens")

    # Embedding
    embedding_model: str = Field(
        default="text-embedding-004",
        description="Embedding model name",
    )
    embedding_dimensions: int = Field(default=768, description="Embedding dimensions")

    # Session Management
    session_max_turns: int = Field(default=50, description="Max conversation turns")
    session_timeout_minutes: int = Field(default=60, description="Session timeout")
    session_max_tokens: int = Field(default=100000, description="Max tokens per session")

    # Safety & Content Filtering
    enable_content_filter: bool = Field(default=True, description="Enable content filtering")
    enable_pii_masking: bool = Field(default=True, description="Enable PII masking")
    max_retries: int = Field(default=3, description="Max retry attempts")

    # Monitoring
    enable_metrics: bool = Field(default=True, description="Enable Prometheus metrics")
    enable_tracing: bool = Field(default=True, description="Enable OpenTelemetry tracing")
    metrics_port: int = Field(default=9090, description="Metrics export port")

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"Invalid log level. Must be one of: {valid_levels}")
        return v_upper

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment == "dev"

    def configure_logging(self) -> None:
        """Configure application logging."""
        logging.basicConfig(
            level=getattr(logging, self.log_level),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
