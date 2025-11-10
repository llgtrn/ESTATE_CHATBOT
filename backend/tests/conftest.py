"""Pytest configuration and fixtures."""
import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import app


@pytest.fixture
def test_settings() -> Settings:
    """Create test settings."""
    return Settings(
        environment="test",
        debug=True,
        log_level="DEBUG",
        database_url="postgresql+asyncpg://test:test@localhost:5432/test",
        redis_url="redis://localhost:6379/1",
        gcp_project_id="test-project",
        langsmith_tracing=False,
    )


@pytest.fixture
def client() -> TestClient:
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def sample_message() -> str:
    """Sample Japanese message."""
    return "東京で2LDKのマンションを探しています。予算は5000万円です。"


@pytest.fixture
def sample_brief_data() -> dict:
    """Sample brief data."""
    return {
        "property_type": "buy",
        "location": "東京",
        "budget": 50000000,
        "rooms": "2LDK",
    }
