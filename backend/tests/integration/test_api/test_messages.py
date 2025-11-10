"""Integration tests for message API endpoints."""
import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.integration
class TestMessagesAPI:
    """Tests for messages API."""

    def test_send_message(self, client: TestClient, sample_message: str) -> None:
        """Test sending a message."""
        session_id = "test_session_123"
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": sample_message, "language": "ja"},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message_id" in data
        assert "response" in data
        assert data["session_id"] == session_id

    def test_send_message_english(self, client: TestClient) -> None:
        """Test sending English message."""
        session_id = "test_session_123"
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": "I am looking for a house", "language": "en"},
        )

        assert response.status_code == status.HTTP_200_OK

    def test_send_empty_message(self, client: TestClient) -> None:
        """Test sending empty message."""
        session_id = "test_session_123"
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": "", "language": "ja"},
        )

        # Should still return 200 with appropriate response
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]

    def test_get_messages(self, client: TestClient) -> None:
        """Test getting session messages."""
        session_id = "test_session_123"
        response = client.get(f"/api/v1/sessions/{session_id}/messages")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "session_id" in data
        assert "messages" in data
        assert isinstance(data["messages"], list)
