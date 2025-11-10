"""Integration tests for glossary API endpoints."""
import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.integration
class TestGlossaryAPI:
    """Tests for glossary API."""

    def test_search_glossary(self, client: TestClient) -> None:
        """Test searching glossary."""
        response = client.get("/api/v1/glossary/search?query=築年数&language=ja")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "query" in data
        assert "results" in data
        assert isinstance(data["results"], list)

    def test_search_glossary_english(self, client: TestClient) -> None:
        """Test searching glossary in English."""
        response = client.get("/api/v1/glossary/search?query=rent&language=en")

        assert response.status_code == status.HTTP_200_OK

    def test_search_glossary_invalid_language(self, client: TestClient) -> None:
        """Test searching with invalid language."""
        response = client.get("/api/v1/glossary/search?query=test&language=invalid")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_term(self, client: TestClient) -> None:
        """Test getting term details."""
        term_id = "term_123"
        response = client.get(f"/api/v1/glossary/terms/{term_id}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "term_id" in data
        assert "term" in data
