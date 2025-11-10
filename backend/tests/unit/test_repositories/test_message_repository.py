"""Tests for message repository."""
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.db.repositories.message import MessageRepository


class TestMessageRepository:
    """Tests for MessageRepository class."""

    @pytest.fixture
    def mock_db(self) -> AsyncMock:
        """Create mock database session."""
        return AsyncMock()

    @pytest.fixture
    def repository(self, mock_db: AsyncMock) -> MessageRepository:
        """Create repository instance."""
        return MessageRepository(mock_db)

    @pytest.mark.asyncio
    async def test_create_basic(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test creating a basic message."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        message = await repository.create(
            session_id="session_123",
            role="user",
            content="Hello",
            language="en",
        )

        assert message is not None
        assert message.session_id == "session_123"
        assert message.role == "user"
        assert message.content == "Hello"
        assert message.language == "en"
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_with_intent(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test creating a message with intent."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        message = await repository.create(
            session_id="session_123",
            role="user",
            content="マンションを買いたい",
            language="ja",
            intent="property_search_buy",
            confidence=0.95,
        )

        assert message.intent == "property_search_buy"
        assert message.confidence == 0.95

    @pytest.mark.asyncio
    async def test_create_with_entities(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test creating a message with entities."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        entities = {"budget": 50000000, "rooms": "3LDK"}
        message = await repository.create(
            session_id="session_123",
            role="user",
            content="予算5000万円で3LDK",
            language="ja",
            entities=entities,
        )

        assert message.entities == entities

    @pytest.mark.asyncio
    async def test_create_with_metadata(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test creating a message with metadata."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        metadata = {"ip_address": "192.168.1.1", "user_agent": "Mozilla/5.0"}
        message = await repository.create(
            session_id="session_123",
            role="user",
            content="Hello",
            metadata=metadata,
        )

        assert message.metadata == metadata

    @pytest.mark.asyncio
    async def test_create_with_token_count(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test creating a message with token count."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        message = await repository.create(
            session_id="session_123",
            role="assistant",
            content="This is a response",
            token_count=150,
        )

        assert message.token_count == 150

    @pytest.mark.asyncio
    async def test_create_defaults_empty_dicts(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test that entities and metadata default to empty dicts."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        message = await repository.create(
            session_id="session_123",
            role="user",
            content="Hello",
        )

        assert message.entities == {}
        assert message.metadata == {}

    @pytest.mark.asyncio
    async def test_get_by_id_exists(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting existing message by ID."""
        mock_message = MagicMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_message
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_id("msg_123")

        assert result == mock_message
        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_id_not_exists(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting non-existent message."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_id("nonexistent")

        assert result is None

    @pytest.mark.asyncio
    async def test_get_by_session_basic(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting messages by session."""
        mock_messages = [MagicMock(), MagicMock(), MagicMock()]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_messages
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_session("session_123")

        assert len(result) == 3
        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_session_with_limit(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting messages with limit."""
        mock_messages = [MagicMock(), MagicMock()]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_messages
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_session("session_123", limit=2)

        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_get_by_session_with_offset(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting messages with offset."""
        mock_messages = [MagicMock()]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_messages
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_session("session_123", offset=5)

        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_get_by_session_with_limit_and_offset(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting messages with both limit and offset."""
        mock_messages = [MagicMock(), MagicMock()]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_messages
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_session("session_123", limit=2, offset=3)

        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_get_by_session_empty(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting messages for session with no messages."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_session("empty_session")

        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_get_recent_messages(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting recent messages."""
        # Mock messages in descending order (most recent first)
        mock_msg1 = MagicMock()
        mock_msg1.created_at = datetime(2024, 1, 1, 12, 0, 2)
        mock_msg2 = MagicMock()
        mock_msg2.created_at = datetime(2024, 1, 1, 12, 0, 1)
        mock_msg3 = MagicMock()
        mock_msg3.created_at = datetime(2024, 1, 1, 12, 0, 0)

        mock_result = MagicMock()
        # Returned in desc order
        mock_result.scalars.return_value.all.return_value = [
            mock_msg1,
            mock_msg2,
            mock_msg3,
        ]
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_recent_messages("session_123", count=3)

        # Should be reversed to chronological order
        assert len(result) == 3
        assert result[0] == mock_msg3  # Oldest first
        assert result[2] == mock_msg1  # Newest last

    @pytest.mark.asyncio
    async def test_get_recent_messages_default_count(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting recent messages with default count."""
        mock_messages = [MagicMock() for _ in range(10)]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_messages
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_recent_messages("session_123")

        assert len(result) == 10

    @pytest.mark.asyncio
    async def test_get_recent_messages_empty(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting recent messages for session with no messages."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_recent_messages("empty_session")

        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_count_by_session(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test counting messages in a session."""
        mock_messages = [MagicMock(), MagicMock(), MagicMock()]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_messages
        mock_db.execute = AsyncMock(return_value=mock_result)

        count = await repository.count_by_session("session_123")

        assert count == 3

    @pytest.mark.asyncio
    async def test_count_by_session_empty(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test counting messages for empty session."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute = AsyncMock(return_value=mock_result)

        count = await repository.count_by_session("empty_session")

        assert count == 0

    @pytest.mark.asyncio
    async def test_get_by_intent(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting messages by intent."""
        mock_messages = [MagicMock(), MagicMock()]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_messages
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_intent("property_search_buy")

        assert len(result) == 2
        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_intent_with_limit(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting messages by intent with custom limit."""
        mock_messages = [MagicMock() for _ in range(50)]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_messages
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_intent("property_search_rent", limit=50)

        assert len(result) == 50

    @pytest.mark.asyncio
    async def test_get_by_intent_no_results(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting messages by intent with no results."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_intent("nonexistent_intent")

        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_update(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test updating a message."""
        mock_message = MagicMock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        result = await repository.update(mock_message)

        assert result == mock_message
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_exists(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test deleting existing message."""
        mock_message = MagicMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_message
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.delete = AsyncMock()
        mock_db.commit = AsyncMock()

        result = await repository.delete("msg_123")

        assert result is True
        mock_db.delete.assert_called_once_with(mock_message)

    @pytest.mark.asyncio
    async def test_delete_not_exists(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test deleting non-existent message."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.delete("nonexistent")

        assert result is False

    @pytest.mark.asyncio
    async def test_create_user_message(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test creating a user message with typical data."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        message = await repository.create(
            session_id="session_123",
            role="user",
            content="東京で3LDKのマンションを探しています。予算は5000万円です。",
            language="ja",
            intent="property_search_buy",
            confidence=0.92,
            entities={"budget": 50000000, "rooms": "3LDK", "location": "東京"},
        )

        assert message.role == "user"
        assert message.intent == "property_search_buy"
        assert message.entities["budget"] == 50000000

    @pytest.mark.asyncio
    async def test_create_assistant_message(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test creating an assistant message."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        message = await repository.create(
            session_id="session_123",
            role="assistant",
            content="東京で3LDK、予算5000万円の物件をお探しですね。",
            language="ja",
            token_count=200,
        )

        assert message.role == "assistant"
        assert message.intent is None  # Assistant messages typically don't have intent
        assert message.token_count == 200

    @pytest.mark.asyncio
    async def test_create_multilingual_messages(
        self, repository: MessageRepository, mock_db: AsyncMock
    ) -> None:
        """Test creating messages in different languages."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        # Japanese
        msg_ja = await repository.create(
            session_id="session_1", role="user", content="こんにちは", language="ja"
        )
        assert msg_ja.language == "ja"

        # English
        msg_en = await repository.create(
            session_id="session_2", role="user", content="Hello", language="en"
        )
        assert msg_en.language == "en"

        # Vietnamese
        msg_vi = await repository.create(
            session_id="session_3", role="user", content="Xin chào", language="vi"
        )
        assert msg_vi.language == "vi"
