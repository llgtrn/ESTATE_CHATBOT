"""Integration tests for brief API endpoints."""
import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.integration
class TestBriefsAPI:
    """Tests for briefs API."""

    def test_get_brief(self, client: TestClient) -> None:
        """Test getting brief details."""
        brief_id = "brief_123"
        response = client.get(f"/api/v1/briefs/{brief_id}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["brief_id"] == brief_id
        assert "status" in data
        assert "property_type" in data

    def test_update_brief(self, client: TestClient) -> None:
        """Test updating brief."""
        brief_id = "brief_123"
        response = client.patch(
            f"/api/v1/briefs/{brief_id}",
            json={"status": "in_progress", "data": {"budget": 50000000}},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["brief_id"] == brief_id

    def test_submit_brief(self, client: TestClient) -> None:
        """Test submitting brief."""
        brief_id = "brief_123"
        response = client.post(f"/api/v1/briefs/{brief_id}/submit")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "submitted"
