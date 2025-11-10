"""Main conversation chain for the chatbot."""
import logging
from typing import Any

logger = logging.getLogger(__name__)


class ConversationChain:
    """Main conversation chain handler."""

    def __init__(self, model_name: str = "gemini-1.5-flash-002") -> None:
        """Initialize conversation chain."""
        self.model_name = model_name
        logger.info(f"Initialized ConversationChain with model: {model_name}")

    async def process_message(self, message: str, context: dict[str, Any]) -> dict[str, Any]:
        """Process a user message and return response."""
        logger.info(f"Processing message: {message[:50]}...")

        # Stub implementation
        return {
            "response": "こんにちは！お探しの物件について教えてください。",
            "intent": "greeting",
            "confidence": 0.95,
        }

    def get_model_info(self) -> dict[str, str]:
        """Get model information."""
        return {"model": self.model_name, "status": "ready"}
