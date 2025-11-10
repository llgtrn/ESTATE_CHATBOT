"""Load tests for the chatbot API."""
from locust import HttpUser, between, task


class ChatbotUser(HttpUser):
    """Simulated chatbot user."""

    wait_time = between(1, 3)
    session_id = None

    def on_start(self) -> None:
        """Initialize user session."""
        response = self.client.post("/api/v1/sessions")
        if response.status_code == 201:
            self.session_id = response.json()["session_id"]

    @task(3)
    def send_message(self) -> None:
        """Send a message to the chatbot."""
        if not self.session_id:
            return

        self.client.post(
            f"/api/v1/sessions/{self.session_id}/messages",
            json={"message": "東京で物件を探しています", "language": "ja"},
        )

    @task(1)
    def get_messages(self) -> None:
        """Get message history."""
        if not self.session_id:
            return

        self.client.get(f"/api/v1/sessions/{self.session_id}/messages")

    @task(1)
    def search_glossary(self) -> None:
        """Search glossary."""
        self.client.get("/api/v1/glossary/search?query=築年数&language=ja")

    def on_stop(self) -> None:
        """Clean up user session."""
        if self.session_id:
            self.client.delete(f"/api/v1/sessions/{self.session_id}")
