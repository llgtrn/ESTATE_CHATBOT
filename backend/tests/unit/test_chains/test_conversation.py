"""Tests for conversation chain."""
import pytest

from app.langchain.chains.conversation import ConversationChain


class TestConversationChain:
    """Tests for ConversationChain class."""

    def test_init(self) -> None:
        """Test chain initialization."""
        chain = ConversationChain()
        assert chain.model_name == "gemini-1.5-flash-002"

    def test_init_custom_model(self) -> None:
        """Test chain initialization with custom model."""
        chain = ConversationChain(model_name="gemini-1.5-pro-002")
        assert chain.model_name == "gemini-1.5-pro-002"

    @pytest.mark.asyncio
    async def test_process_message(self) -> None:
        """Test message processing."""
        chain = ConversationChain()
        context = {"session_id": "test_123"}

        result = await chain.process_message("こんにちは", context)

        assert "response" in result
        assert "intent" in result
        assert "confidence" in result
        assert isinstance(result["response"], str)
        assert isinstance(result["confidence"], float)

    @pytest.mark.asyncio
    async def test_process_empty_message(self) -> None:
        """Test processing empty message."""
        chain = ConversationChain()
        result = await chain.process_message("", {})

        assert "response" in result

    def test_get_model_info(self) -> None:
        """Test getting model info."""
        chain = ConversationChain()
        info = chain.get_model_info()

        assert info["model"] == "gemini-1.5-flash-002"
        assert info["status"] == "ready"

    def test_get_model_info_custom_model(self) -> None:
        """Test getting model info for custom model."""
        chain = ConversationChain(model_name="test-model")
        info = chain.get_model_info()

        assert info["model"] == "test-model"
