"""Tests for conversation service."""
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.core.exceptions import (
    InvalidMessageError,
    SessionExpiredError,
    SessionNotFoundError,
)
from app.db.models import SessionStatus
from app.services.conversation_service import ConversationService


class TestConversationService:
    """Tests for ConversationService class."""

    @pytest.fixture
    def mock_session_repo(self) -> AsyncMock:
        """Create mock session repository."""
        return AsyncMock()

    @pytest.fixture
    def mock_message_repo(self) -> AsyncMock:
        """Create mock message repository."""
        return AsyncMock()

    @pytest.fixture
    def mock_conversation_chain(self) -> AsyncMock:
        """Create mock conversation chain."""
        return AsyncMock()

    @pytest.fixture
    def mock_nlu_service(self) -> AsyncMock:
        """Create mock NLU service."""
        return AsyncMock()

    @pytest.fixture
    def service(
        self,
        mock_session_repo: AsyncMock,
        mock_message_repo: AsyncMock,
        mock_conversation_chain: AsyncMock,
        mock_nlu_service: AsyncMock,
    ) -> ConversationService:
        """Create conversation service instance."""
        return ConversationService(
            session_repo=mock_session_repo,
            message_repo=mock_message_repo,
            conversation_chain=mock_conversation_chain,
            nlu_service=mock_nlu_service,
        )

    @pytest.mark.asyncio
    async def test_create_session_default(
        self, service: ConversationService, mock_session_repo: AsyncMock
    ) -> None:
        """Test creating a session with default parameters."""
        mock_session = MagicMock()
        mock_session.id = "session_123"
        mock_session.status = SessionStatus.ACTIVE
        mock_session.language = "ja"
        mock_session.created_at = datetime.utcnow()
        mock_session.expires_at = None
        mock_session_repo.create.return_value = mock_session

        result = await service.create_session()

        assert result["session_id"] == "session_123"
        assert result["status"] == "active"
        assert result["language"] == "ja"
        mock_session_repo.create.assert_called_once_with(
            language="ja", user_id=None, metadata={}
        )

    @pytest.mark.asyncio
    async def test_create_session_with_user_id(
        self, service: ConversationService, mock_session_repo: AsyncMock
    ) -> None:
        """Test creating a session with user ID."""
        mock_session = MagicMock()
        mock_session.id = "session_123"
        mock_session.status = SessionStatus.ACTIVE
        mock_session.language = "en"
        mock_session.created_at = datetime.utcnow()
        mock_session.expires_at = None
        mock_session_repo.create.return_value = mock_session

        result = await service.create_session(language="en", user_id="user_456")

        assert result["session_id"] == "session_123"
        mock_session_repo.create.assert_called_once_with(
            language="en", user_id="user_456", metadata={}
        )

    @pytest.mark.asyncio
    async def test_create_session_with_metadata(
        self, service: ConversationService, mock_session_repo: AsyncMock
    ) -> None:
        """Test creating a session with metadata."""
        mock_session = MagicMock()
        mock_session.id = "session_123"
        mock_session.status = SessionStatus.ACTIVE
        mock_session.language = "ja"
        mock_session.created_at = datetime.utcnow()
        mock_session.expires_at = None
        mock_session_repo.create.return_value = mock_session

        metadata = {"source": "web", "device": "mobile"}
        result = await service.create_session(metadata=metadata)

        mock_session_repo.create.assert_called_once_with(
            language="ja", user_id=None, metadata=metadata
        )

    @pytest.mark.asyncio
    async def test_get_session_success(
        self, service: ConversationService, mock_session_repo: AsyncMock
    ) -> None:
        """Test getting existing session."""
        mock_session = MagicMock()
        mock_session.id = "session_123"
        mock_session.status = SessionStatus.ACTIVE
        mock_session.language = "ja"
        mock_session.turn_count = 5
        mock_session.token_count = 100
        mock_session.created_at = datetime.utcnow()
        mock_session.updated_at = datetime.utcnow()
        mock_session_repo.get_by_id.return_value = mock_session

        result = await service.get_session("session_123")

        assert result["session_id"] == "session_123"
        assert result["status"] == "active"
        assert result["turn_count"] == 5
        assert result["token_count"] == 100

    @pytest.mark.asyncio
    async def test_get_session_not_found(
        self, service: ConversationService, mock_session_repo: AsyncMock
    ) -> None:
        """Test getting non-existent session."""
        mock_session_repo.get_by_id.return_value = None

        with pytest.raises(SessionNotFoundError):
            await service.get_session("nonexistent")

    @pytest.mark.asyncio
    async def test_get_session_expired(
        self, service: ConversationService, mock_session_repo: AsyncMock
    ) -> None:
        """Test getting expired session."""
        mock_session = MagicMock()
        mock_session.status = SessionStatus.EXPIRED
        mock_session_repo.get_by_id.return_value = mock_session

        with pytest.raises(SessionExpiredError):
            await service.get_session("session_123")

    @pytest.mark.asyncio
    async def test_send_message_success(
        self,
        service: ConversationService,
        mock_session_repo: AsyncMock,
        mock_message_repo: AsyncMock,
        mock_conversation_chain: AsyncMock,
        mock_nlu_service: AsyncMock,
    ) -> None:
        """Test sending a message successfully."""
        # Mock session
        mock_session = MagicMock()
        mock_session.id = "session_123"
        mock_session.status = SessionStatus.ACTIVE
        mock_session_repo.get_by_id.return_value = mock_session

        # Mock NLU result
        mock_nlu_service.analyze.return_value = {
            "intent": "property_search_buy",
            "confidence": 0.95,
            "entities": {"budget": 50000000},
        }

        # Mock user message
        mock_user_message = MagicMock()
        mock_user_message.id = "msg_user_123"
        mock_message_repo.create.return_value = mock_user_message

        # Mock conversation history
        mock_message_repo.get_recent_messages.return_value = []

        # Mock assistant response
        mock_conversation_chain.process_message.return_value = {
            "response": "マンション購入のお手伝いをいたします。"
        }

        # Mock assistant message
        mock_assistant_message = MagicMock()
        mock_assistant_message.id = "msg_asst_123"

        # Configure create to return user message first, then assistant message
        mock_message_repo.create.side_effect = [
            mock_user_message,
            mock_assistant_message,
        ]

        result = await service.send_message(
            session_id="session_123",
            message="マンションを買いたいです",
            language="ja",
        )

        assert result["session_id"] == "session_123"
        assert result["message_id"] == "msg_asst_123"
        assert result["response"] == "マンション購入のお手伝いをいたします。"
        assert result["intent"] == "property_search_buy"
        assert result["confidence"] == 0.95
        assert result["entities"] == {"budget": 50000000}
        mock_session_repo.increment_turn_count.assert_called_once_with("session_123")

    @pytest.mark.asyncio
    async def test_send_message_session_not_found(
        self, service: ConversationService, mock_session_repo: AsyncMock
    ) -> None:
        """Test sending message to non-existent session."""
        mock_session_repo.get_by_id.return_value = None

        with pytest.raises(SessionNotFoundError):
            await service.send_message("nonexistent", "Hello")

    @pytest.mark.asyncio
    async def test_send_message_session_expired(
        self, service: ConversationService, mock_session_repo: AsyncMock
    ) -> None:
        """Test sending message to expired session."""
        mock_session = MagicMock()
        mock_session.status = SessionStatus.COMPLETED
        mock_session_repo.get_by_id.return_value = mock_session

        with pytest.raises(SessionExpiredError):
            await service.send_message("session_123", "Hello")

    @pytest.mark.asyncio
    async def test_send_message_empty_message(
        self, service: ConversationService, mock_session_repo: AsyncMock
    ) -> None:
        """Test sending empty message."""
        mock_session = MagicMock()
        mock_session.status = SessionStatus.ACTIVE
        mock_session_repo.get_by_id.return_value = mock_session

        with pytest.raises(InvalidMessageError):
            await service.send_message("session_123", "")

    @pytest.mark.asyncio
    async def test_send_message_whitespace_only(
        self, service: ConversationService, mock_session_repo: AsyncMock
    ) -> None:
        """Test sending whitespace-only message."""
        mock_session = MagicMock()
        mock_session.status = SessionStatus.ACTIVE
        mock_session_repo.get_by_id.return_value = mock_session

        with pytest.raises(InvalidMessageError):
            await service.send_message("session_123", "   ")

    @pytest.mark.asyncio
    async def test_send_message_auto_language_detection(
        self,
        service: ConversationService,
        mock_session_repo: AsyncMock,
        mock_message_repo: AsyncMock,
        mock_conversation_chain: AsyncMock,
        mock_nlu_service: AsyncMock,
    ) -> None:
        """Test sending message with automatic language detection."""
        mock_session = MagicMock()
        mock_session.status = SessionStatus.ACTIVE
        mock_session_repo.get_by_id.return_value = mock_session

        mock_nlu_service.analyze.return_value = {
            "intent": "greeting",
            "confidence": 0.9,
            "entities": {},
        }

        mock_user_message = MagicMock()
        mock_assistant_message = MagicMock()
        mock_assistant_message.id = "msg_123"
        mock_message_repo.create.side_effect = [
            mock_user_message,
            mock_assistant_message,
        ]
        mock_message_repo.get_recent_messages.return_value = []

        mock_conversation_chain.process_message.return_value = {
            "response": "Hello! How can I help you?"
        }

        # Send English message without specifying language
        result = await service.send_message("session_123", "Hello")

        assert result["language"] == "en"

    @pytest.mark.asyncio
    async def test_send_message_with_conversation_history(
        self,
        service: ConversationService,
        mock_session_repo: AsyncMock,
        mock_message_repo: AsyncMock,
        mock_conversation_chain: AsyncMock,
        mock_nlu_service: AsyncMock,
    ) -> None:
        """Test sending message with conversation history."""
        mock_session = MagicMock()
        mock_session.status = SessionStatus.ACTIVE
        mock_session_repo.get_by_id.return_value = mock_session

        # Mock history messages
        mock_history_msg1 = MagicMock()
        mock_history_msg1.role = "user"
        mock_history_msg1.content = "Previous message"
        mock_history_msg2 = MagicMock()
        mock_history_msg2.role = "assistant"
        mock_history_msg2.content = "Previous response"
        mock_message_repo.get_recent_messages.return_value = [
            mock_history_msg1,
            mock_history_msg2,
        ]

        mock_nlu_service.analyze.return_value = {
            "intent": "property_search_rent",
            "confidence": 0.88,
            "entities": {"rooms": "2LDK"},
        }

        mock_user_message = MagicMock()
        mock_assistant_message = MagicMock()
        mock_assistant_message.id = "msg_123"
        mock_message_repo.create.side_effect = [
            mock_user_message,
            mock_assistant_message,
        ]

        mock_conversation_chain.process_message.return_value = {
            "response": "Response with context"
        }

        await service.send_message("session_123", "賃貸を探しています", language="ja")

        # Verify history was passed to conversation chain
        call_args = mock_conversation_chain.process_message.call_args
        context = call_args[0][1]
        assert len(context["history"]) == 2
        assert context["history"][0]["role"] == "user"
        assert context["history"][0]["content"] == "Previous message"

    @pytest.mark.asyncio
    async def test_get_messages_success(
        self,
        service: ConversationService,
        mock_session_repo: AsyncMock,
        mock_message_repo: AsyncMock,
    ) -> None:
        """Test getting messages for a session."""
        mock_session = MagicMock()
        mock_session_repo.get_by_id.return_value = mock_session

        mock_msg1 = MagicMock()
        mock_msg1.id = "msg_1"
        mock_msg1.role = "user"
        mock_msg1.content = "Hello"
        mock_msg1.language = "en"
        mock_msg1.intent = "greeting"
        mock_msg1.confidence = 0.9
        mock_msg1.entities = {}
        mock_msg1.created_at = datetime.utcnow()

        mock_msg2 = MagicMock()
        mock_msg2.id = "msg_2"
        mock_msg2.role = "assistant"
        mock_msg2.content = "Hi there!"
        mock_msg2.language = "en"
        mock_msg2.intent = None
        mock_msg2.confidence = None
        mock_msg2.entities = {}
        mock_msg2.created_at = datetime.utcnow()

        mock_message_repo.get_by_session.return_value = [mock_msg1, mock_msg2]
        mock_message_repo.count_by_session.return_value = 2

        result = await service.get_messages("session_123", limit=10, offset=0)

        assert result["session_id"] == "session_123"
        assert len(result["messages"]) == 2
        assert result["total"] == 2
        assert result["limit"] == 10
        assert result["offset"] == 0

    @pytest.mark.asyncio
    async def test_get_messages_session_not_found(
        self, service: ConversationService, mock_session_repo: AsyncMock
    ) -> None:
        """Test getting messages for non-existent session."""
        mock_session_repo.get_by_id.return_value = None

        with pytest.raises(SessionNotFoundError):
            await service.get_messages("nonexistent")

    @pytest.mark.asyncio
    async def test_get_messages_with_pagination(
        self,
        service: ConversationService,
        mock_session_repo: AsyncMock,
        mock_message_repo: AsyncMock,
    ) -> None:
        """Test getting messages with pagination."""
        mock_session = MagicMock()
        mock_session_repo.get_by_id.return_value = mock_session

        mock_message_repo.get_by_session.return_value = []
        mock_message_repo.count_by_session.return_value = 100

        result = await service.get_messages("session_123", limit=20, offset=40)

        assert result["limit"] == 20
        assert result["offset"] == 40
        assert result["total"] == 100
        mock_message_repo.get_by_session.assert_called_once_with(
            session_id="session_123", limit=20, offset=40
        )

    @pytest.mark.asyncio
    async def test_delete_session_success(
        self, service: ConversationService, mock_session_repo: AsyncMock
    ) -> None:
        """Test deleting a session."""
        mock_session_repo.delete.return_value = True

        result = await service.delete_session("session_123")

        assert result is True
        mock_session_repo.delete.assert_called_once_with("session_123")

    @pytest.mark.asyncio
    async def test_delete_session_not_found(
        self, service: ConversationService, mock_session_repo: AsyncMock
    ) -> None:
        """Test deleting non-existent session."""
        mock_session_repo.delete.return_value = False

        result = await service.delete_session("nonexistent")

        assert result is False

    @pytest.mark.asyncio
    async def test_cleanup_expired_sessions(
        self, service: ConversationService, mock_session_repo: AsyncMock
    ) -> None:
        """Test cleaning up expired sessions."""
        mock_session_repo.cleanup_expired_sessions.return_value = 5

        result = await service.cleanup_expired_sessions()

        assert result == 5
        mock_session_repo.cleanup_expired_sessions.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_message_vietnamese(
        self,
        service: ConversationService,
        mock_session_repo: AsyncMock,
        mock_message_repo: AsyncMock,
        mock_conversation_chain: AsyncMock,
        mock_nlu_service: AsyncMock,
    ) -> None:
        """Test sending Vietnamese message."""
        mock_session = MagicMock()
        mock_session.status = SessionStatus.ACTIVE
        mock_session_repo.get_by_id.return_value = mock_session

        mock_nlu_service.analyze.return_value = {
            "intent": "property_search_rent",
            "confidence": 0.85,
            "entities": {},
        }

        mock_user_message = MagicMock()
        mock_assistant_message = MagicMock()
        mock_assistant_message.id = "msg_123"
        mock_message_repo.create.side_effect = [
            mock_user_message,
            mock_assistant_message,
        ]
        mock_message_repo.get_recent_messages.return_value = []

        mock_conversation_chain.process_message.return_value = {
            "response": "Tôi có thể giúp bạn tìm nhà"
        }

        result = await service.send_message(
            "session_123", "Tôi muốn thuê căn hộ", language="vi"
        )

        assert result["language"] == "vi"
        assert result["response"] == "Tôi có thể giúp bạn tìm nhà"

    @pytest.mark.asyncio
    async def test_send_message_with_entities(
        self,
        service: ConversationService,
        mock_session_repo: AsyncMock,
        mock_message_repo: AsyncMock,
        mock_conversation_chain: AsyncMock,
        mock_nlu_service: AsyncMock,
    ) -> None:
        """Test sending message with extracted entities."""
        mock_session = MagicMock()
        mock_session.status = SessionStatus.ACTIVE
        mock_session_repo.get_by_id.return_value = mock_session

        # NLU extracts multiple entities
        mock_nlu_service.analyze.return_value = {
            "intent": "property_search_buy",
            "confidence": 0.92,
            "entities": {
                "budget": 80000000,
                "rooms": "3LDK",
                "location": "渋谷区",
                "area": 80.5,
            },
        }

        mock_user_message = MagicMock()
        mock_user_message.id = "msg_user_123"
        mock_assistant_message = MagicMock()
        mock_assistant_message.id = "msg_asst_123"
        mock_message_repo.create.side_effect = [
            mock_user_message,
            mock_assistant_message,
        ]
        mock_message_repo.get_recent_messages.return_value = []

        mock_conversation_chain.process_message.return_value = {
            "response": "渋谷区で3LDK、80㎡、予算8000万円の物件をお探しですね。"
        }

        result = await service.send_message(
            "session_123", "渋谷区で3LDK、80㎡、予算8000万円の物件を探しています", language="ja"
        )

        # Verify entities were saved with user message
        user_message_call = mock_message_repo.create.call_args_list[0]
        assert user_message_call[1]["entities"]["budget"] == 80000000
        assert user_message_call[1]["entities"]["rooms"] == "3LDK"
        assert user_message_call[1]["entities"]["location"] == "渋谷区"

        # Verify entities are returned in response
        assert result["entities"]["budget"] == 80000000
        assert result["entities"]["rooms"] == "3LDK"
