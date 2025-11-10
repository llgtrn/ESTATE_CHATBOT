"""Integration tests for session API endpoints."""
import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.integration
class TestSessionsAPI:
    """Tests for sessions API."""

    def test_create_session(self, client: TestClient) -> None:
        """Test creating a new session."""
        response = client.post("/api/v1/sessions")

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "session_id" in data
        assert "status" in data
        assert data["status"] == "active"

    def test_get_session(self, client: TestClient) -> None:
        """Test getting session details."""
        session_id = "test_session_123"
        response = client.get(f"/api/v1/sessions/{session_id}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["session_id"] == session_id
        assert "status" in data

    def test_delete_session(self, client: TestClient) -> None:
        """Test deleting a session."""
        session_id = "test_session_123"
        response = client.delete(f"/api/v1/sessions/{session_id}")

        assert response.status_code == status.HTTP_204_NO_CONTENT
