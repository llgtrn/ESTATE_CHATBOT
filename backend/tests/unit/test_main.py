"""Tests for main application."""
from fastapi import status
from fastapi.testclient import TestClient


class TestMainApp:
    """Tests for main FastAPI application."""

    def test_health_check(self, client: TestClient) -> None:
        """Test health check endpoint."""
        response = client.get("/health")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data

    def test_root_endpoint(self, client: TestClient) -> None:
        """Test root endpoint."""
        response = client.get("/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "environment" in data

    def test_docs_endpoint(self, client: TestClient) -> None:
        """Test API documentation endpoint."""
        response = client.get("/docs")

        # Docs may be disabled in production
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

    def test_openapi_schema(self, client: TestClient) -> None:
        """Test OpenAPI schema endpoint."""
        response = client.get("/openapi.json")

        assert response.status_code == status.HTTP_200_OK
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema

    def test_metrics_endpoint(self, client: TestClient) -> None:
        """Test Prometheus metrics endpoint."""
        response = client.get("/metrics")

        # Metrics endpoint should be accessible
        assert response.status_code == status.HTTP_200_OK
