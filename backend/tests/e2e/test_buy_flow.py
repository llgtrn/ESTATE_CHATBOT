"""End-to-end tests for buy property flow."""
import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.e2e
class TestBuyFlow:
    """E2E tests for buying property flow."""

    def test_complete_buy_flow(self, client: TestClient) -> None:
        """Test complete buy property flow from start to finish."""
        # Step 1: Create session
        response = client.post("/api/v1/sessions")
        assert response.status_code == status.HTTP_201_CREATED
        session_data = response.json()
        session_id = session_data["session_id"]

        # Step 2: Send initial message
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={
                "message": "東京で2LDKのマンションを買いたいです。予算は5000万円です。",
                "language": "ja",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        message_data = response.json()
        assert "response" in message_data

        # Step 3: Continue conversation
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": "駅近が良いです", "language": "ja"},
        )
        assert response.status_code == status.HTTP_200_OK

        # Step 4: Get message history
        response = client.get(f"/api/v1/sessions/{session_id}/messages")
        assert response.status_code == status.HTTP_200_OK

        # Step 5: Clean up - delete session
        response = client.delete(f"/api/v1/sessions/{session_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_brief_creation_flow(self, client: TestClient) -> None:
        """Test brief creation during buy flow."""
        # Create session
        response = client.post("/api/v1/sessions")
        session_id = response.json()["session_id"]

        # Send messages to populate brief
        messages = [
            "マンションを買いたいです",
            "予算は5000万円です",
            "2LDKが良いです",
            "東京23区内で探しています",
        ]

        for message in messages:
            response = client.post(
                f"/api/v1/sessions/{session_id}/messages",
                json={"message": message, "language": "ja"},
            )
            assert response.status_code == status.HTTP_200_OK
