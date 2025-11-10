"""End-to-end tests for sell property flow."""
import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.e2e
class TestSellFlow:
    """E2E tests for selling property flow."""

    def test_complete_sell_flow(self, client: TestClient) -> None:
        """Test complete sell property flow from start to finish."""
        # Step 1: Create session
        response = client.post("/api/v1/sessions")
        assert response.status_code == status.HTTP_201_CREATED
        session_data = response.json()
        session_id = session_data["session_id"]

        # Step 2: Express sell intent
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={
                "message": "マンションを売却したいです",
                "language": "ja",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        message_data = response.json()
        assert "response" in message_data

        # Step 3: Provide property location
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": "東京都港区にあります", "language": "ja"},
        )
        assert response.status_code == status.HTTP_200_OK

        # Step 4: Provide property details
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": "3LDKで築15年です", "language": "ja"},
        )
        assert response.status_code == status.HTTP_200_OK

        # Step 5: Provide area information
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": "専有面積は80㎡です", "language": "ja"},
        )
        assert response.status_code == status.HTTP_200_OK

        # Step 6: Provide price expectation
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": "8000万円くらいで売りたいです", "language": "ja"},
        )
        assert response.status_code == status.HTTP_200_OK

        # Step 7: Get conversation history
        response = client.get(f"/api/v1/sessions/{session_id}/messages")
        assert response.status_code == status.HTTP_200_OK
        history_data = response.json()
        assert history_data["total"] >= 10  # Multiple messages exchanged

        # Step 8: Confirm details
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": "査定をお願いします", "language": "ja"},
        )
        assert response.status_code == status.HTTP_200_OK

        # Step 9: Clean up
        response = client.delete(f"/api/v1/sessions/{session_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_sell_flow_with_urgency(self, client: TestClient) -> None:
        """Test sell flow with urgency."""
        # Create session
        response = client.post("/api/v1/sessions")
        session_id = response.json()["session_id"]

        # Urgent sale
        messages = [
            "急いでマンションを売りたいです",
            "3ヶ月以内に売却したい",
            "渋谷区のマンションです",
            "2LDK、70㎡",
            "希望価格は7000万円",
        ]

        for message in messages:
            response = client.post(
                f"/api/v1/sessions/{session_id}/messages",
                json={"message": message, "language": "ja"},
            )
            assert response.status_code == status.HTTP_200_OK

    def test_sell_flow_inherited_property(self, client: TestClient) -> None:
        """Test sell flow for inherited property."""
        # Create session
        response = client.post("/api/v1/sessions")
        session_id = response.json()["session_id"]

        # Inherited property details
        messages = [
            "相続した一戸建てを売却したい",
            "横浜市にあります",
            "築30年です",
            "土地面積は100㎡",
            "建物面積は120㎡",
            "相場を知りたいです",
        ]

        for message in messages:
            response = client.post(
                f"/api/v1/sessions/{session_id}/messages",
                json={"message": message, "language": "ja"},
            )
            assert response.status_code == status.HTTP_200_OK

    def test_sell_flow_multiple_properties(self, client: TestClient) -> None:
        """Test sell flow for multiple properties."""
        # Create session
        response = client.post("/api/v1/sessions")
        session_id = response.json()["session_id"]

        # First property
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": "2つの物件を売りたいです", "language": "ja"},
        )
        assert response.status_code == status.HTTP_200_OK

        # Property 1 details
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": "1つ目は渋谷区のマンション、2LDK", "language": "ja"},
        )
        assert response.status_code == status.HTTP_200_OK

        # Property 2 details
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": "2つ目は目黒区の一戸建て", "language": "ja"},
        )
        assert response.status_code == status.HTTP_200_OK

    def test_sell_flow_with_english(self, client: TestClient) -> None:
        """Test sell flow in English."""
        # Create session
        response = client.post("/api/v1/sessions")
        session_id = response.json()["session_id"]

        # Express intent in English
        messages = [
            "I want to sell my apartment",
            "It's located in Shibuya, Tokyo",
            "2 bedrooms, 75 square meters",
            "Built 10 years ago",
            "I hope to get around 70 million yen",
        ]

        for message in messages:
            response = client.post(
                f"/api/v1/sessions/{session_id}/messages",
                json={"message": message, "language": "en"},
            )
            assert response.status_code == status.HTTP_200_OK

    def test_sell_flow_price_negotiation(self, client: TestClient) -> None:
        """Test sell flow with price discussion."""
        # Create session
        response = client.post("/api/v1/sessions")
        session_id = response.json()["session_id"]

        # Initial price
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": "マンションを1億円で売りたい", "language": "ja"},
        )
        assert response.status_code == status.HTTP_200_OK

        # Price flexibility
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": "9000万円でも考えます", "language": "ja"},
        )
        assert response.status_code == status.HTTP_200_OK

        # Minimum price
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"message": "最低でも8500万円は欲しいです", "language": "ja"},
        )
        assert response.status_code == status.HTTP_200_OK

    def test_sell_flow_with_loan_balance(self, client: TestClient) -> None:
        """Test sell flow with outstanding loan."""
        # Create session
        response = client.post("/api/v1/sessions")
        session_id = response.json()["session_id"]

        # Property with loan
        messages = [
            "住宅ローンが残っているマンションを売りたい",
            "ローン残高は2000万円です",
            "売却価格5000万円を希望",
            "世田谷区の物件です",
        ]

        for message in messages:
            response = client.post(
                f"/api/v1/sessions/{session_id}/messages",
                json={"message": message, "language": "ja"},
            )
            assert response.status_code == status.HTTP_200_OK

    def test_sell_flow_renovation_inquiry(self, client: TestClient) -> None:
        """Test sell flow with renovation consideration."""
        # Create session
        response = client.post("/api/v1/sessions")
        session_id = response.json()["session_id"]

        # Renovation consideration
        messages = [
            "古いマンションを売りたい",
            "リノベーションしたほうがいいですか",
            "築25年です",
            "設備は古いままです",
        ]

        for message in messages:
            response = client.post(
                f"/api/v1/sessions/{session_id}/messages",
                json={"message": message, "language": "ja"},
            )
            assert response.status_code == status.HTTP_200_OK

    def test_sell_flow_tax_inquiry(self, client: TestClient) -> None:
        """Test sell flow with tax questions."""
        # Create session
        response = client.post("/api/v1/sessions")
        session_id = response.json()["session_id"]

        # Tax-related questions
        messages = [
            "マンション売却を考えています",
            "税金はどのくらいかかりますか",
            "購入価格は6000万円でした",
            "10年前に購入しました",
        ]

        for message in messages:
            response = client.post(
                f"/api/v1/sessions/{session_id}/messages",
                json={"message": message, "language": "ja"},
            )
            assert response.status_code == status.HTTP_200_OK
