"""End-to-end tests for rent property flow."""
import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.e2e
class TestRentFlow:
    """E2E tests for renting property flow."""

    def test_complete_rent_flow(self, client: TestClient) -> None:
        """Test complete rent property flow from start to finish."""
        # Step 1: Create session
        response = client.post("/api/v1/sessions")
        assert response.status_code == status.HTTP_201_CREATED
        session_data = response.json()
        session_id = session_data["session_id"]

        # Step 2: Send initial message - express rent intent
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={
                "message": "賃貸物件を探しています。予算は月15万円です。",
                "language": "ja",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        message_data = response.json()
        assert "response" in message_data
        # Should detect rent intent and budget
        assert message_data.get("intent") in ["property_search_rent", None]

        # Step 3: Provide location
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": "渋谷区がいいです", "language": "ja"},
        )
        assert response.status_code == status.HTTP_200_OK

        # Step 4: Provide room requirements
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": "1LDKか2LDKを希望します", "language": "ja"},
        )
        assert response.status_code == status.HTTP_200_OK

        # Step 5: Provide additional requirements
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": "駅から徒歩5分以内でペット可が良いです", "language": "ja"},
        )
        assert response.status_code == status.HTTP_200_OK

        # Step 6: Get conversation history
        response = client.get(f"/api/v1/sessions/{session_id}/messages")
        assert response.status_code == status.HTTP_200_OK
        history_data = response.json()
        # Should have at least 8 messages (4 user + 4 assistant)
        assert history_data["total"] >= 8

        # Step 7: Confirm details
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": "はい、この条件で探してください", "language": "ja"},
        )
        assert response.status_code == status.HTTP_200_OK

        # Step 8: Clean up - delete session
        response = client.delete(f"/api/v1/sessions/{session_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_rent_flow_with_english(self, client: TestClient) -> None:
        """Test rent flow in English."""
        # Create session
        response = client.post("/api/v1/sessions")
        session_id = response.json()["session_id"]

        # Express intent in English
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={
                "message": "I'm looking for an apartment to rent in Tokyo",
                "language": "en",
            },
        )
        assert response.status_code == status.HTTP_200_OK

        # Provide budget
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": "My budget is 150,000 yen per month", "language": "en"},
        )
        assert response.status_code == status.HTTP_200_OK

        # Provide requirements
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": "I need 2 bedrooms near a station", "language": "en"},
        )
        assert response.status_code == status.HTTP_200_OK

    def test_rent_flow_short_term(self, client: TestClient) -> None:
        """Test rent flow for short-term rental."""
        # Create session
        response = client.post("/api/v1/sessions")
        session_id = response.json()["session_id"]

        # Messages about short-term rental
        messages = [
            "3ヶ月だけ借りたいです",
            "品川区で探しています",
            "家具付きがいいです",
            "予算は月20万円まで",
        ]

        for message in messages:
            response = client.post(
                f"/api/v1/sessions/{session_id}/messages",
                json={"message": message, "language": "ja"},
            )
            assert response.status_code == status.HTTP_200_OK

    def test_rent_flow_with_specific_building(self, client: TestClient) -> None:
        """Test rent flow with specific building requirements."""
        # Create session
        response = client.post("/api/v1/sessions")
        session_id = response.json()["session_id"]

        # Detailed requirements
        messages = [
            "賃貸マンションを探しています",
            "予算は月18万円です",
            "新宿区希望です",
            "築10年以内",
            "オートロック付き",
            "2階以上",
            "南向き",
        ]

        for message in messages:
            response = client.post(
                f"/api/v1/sessions/{session_id}/messages",
                json={"message": message, "language": "ja"},
            )
            assert response.status_code == status.HTTP_200_OK

        # Get history
        response = client.get(f"/api/v1/sessions/{session_id}/messages")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["total"] >= 14  # 7 user + 7 assistant

    def test_rent_flow_budget_adjustment(self, client: TestClient) -> None:
        """Test rent flow with budget adjustment."""
        # Create session
        response = client.post("/api/v1/sessions")
        session_id = response.json()["session_id"]

        # Initial budget
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": "予算は月10万円で賃貸を探しています", "language": "ja"},
        )
        assert response.status_code == status.HTTP_200_OK

        # Adjust budget
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": "やはり月12万円まで出せます", "language": "ja"},
        )
        assert response.status_code == status.HTTP_200_OK

        # Further adjustment
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": "最大で月15万円までなら大丈夫です", "language": "ja"},
        )
        assert response.status_code == status.HTTP_200_OK

    def test_rent_flow_multiple_locations(self, client: TestClient) -> None:
        """Test rent flow with multiple location preferences."""
        # Create session
        response = client.post("/api/v1/sessions")
        session_id = response.json()["session_id"]

        # Multiple locations
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={
                "message": "渋谷区か目黒区で賃貸を探しています。予算は月20万円です。",
                "language": "ja",
            },
        )
        assert response.status_code == status.HTTP_200_OK

        # Additional location
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": "世田谷区でも良いです", "language": "ja"},
        )
        assert response.status_code == status.HTTP_200_OK

    def test_rent_flow_with_glossary_inquiry(self, client: TestClient) -> None:
        """Test rent flow with glossary term inquiry."""
        # Create session
        response = client.post("/api/v1/sessions")
        session_id = response.json()["session_id"]

        # Ask about rent
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": "賃貸を探しています", "language": "ja"},
        )
        assert response.status_code == status.HTTP_200_OK

        # Ask about glossary term
        response = client.get("/api/v1/glossary/search?query=敷金&language=ja")
        assert response.status_code == status.HTTP_200_OK

        # Continue conversation
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": "敷金なしの物件を探しています", "language": "ja"},
        )
        assert response.status_code == status.HTTP_200_OK
