"""Tests for session repository."""
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.db.models import SessionStatus
from app.db.repositories.session import SessionRepository


class TestSessionRepository:
    """Tests for SessionRepository class."""

    @pytest.fixture
    def mock_db(self) -> AsyncMock:
        """Create mock database session."""
        return AsyncMock()

    @pytest.fixture
    def repository(self, mock_db: AsyncMock) -> SessionRepository:
        """Create repository instance."""
        return SessionRepository(mock_db)

    @pytest.mark.asyncio
    async def test_create(self, repository: SessionRepository, mock_db: AsyncMock) -> None:
        """Test creating a session."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        session = await repository.create(language="ja")

        assert session is not None
        assert session.language == "ja"
        assert session.status == SessionStatus.ACTIVE
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_with_user_id(
        self, repository: SessionRepository, mock_db: AsyncMock
    ) -> None:
        """Test creating a session with user ID."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        session = await repository.create(user_id="user_123")

        assert session.user_id == "user_123"

    @pytest.mark.asyncio
    async def test_create_with_metadata(
        self, repository: SessionRepository, mock_db: AsyncMock
    ) -> None:
        """Test creating a session with metadata."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        metadata = {"source": "web", "device": "mobile"}
        session = await repository.create(metadata=metadata)

        assert session.metadata == metadata

    @pytest.mark.asyncio
    async def test_create_with_timeout(
        self, repository: SessionRepository, mock_db: AsyncMock
    ) -> None:
        """Test creating a session with timeout."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        session = await repository.create(timeout_minutes=30)

        assert session.expires_at is not None
        # Check expires_at is approximately 30 minutes from now
        assert session.expires_at > datetime.utcnow()

    @pytest.mark.asyncio
    async def test_get_by_id_exists(
        self, repository: SessionRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting existing session by ID."""
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_session
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_id("session_123")

        assert result == mock_session
        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_id_not_exists(
        self, repository: SessionRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting non-existent session."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_id("nonexistent")

        assert result is None

    @pytest.mark.asyncio
    async def test_update(self, repository: SessionRepository, mock_db: AsyncMock) -> None:
        """Test updating a session."""
        mock_session = MagicMock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        result = await repository.update(mock_session)

        assert result == mock_session
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_status(
        self, repository: SessionRepository, mock_db: AsyncMock
    ) -> None:
        """Test updating session status."""
        mock_session = MagicMock()
        mock_session.status = SessionStatus.ACTIVE
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_session
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        result = await repository.update_status("session_123", SessionStatus.COMPLETED)

        assert mock_session.status == SessionStatus.COMPLETED

    @pytest.mark.asyncio
    async def test_increment_turn_count(
        self, repository: SessionRepository, mock_db: AsyncMock
    ) -> None:
        """Test incrementing turn count."""
        mock_session = MagicMock()
        mock_session.turn_count = 5
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_session
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        await repository.increment_turn_count("session_123")

        assert mock_session.turn_count == 6

    @pytest.mark.asyncio
    async def test_increment_token_count(
        self, repository: SessionRepository, mock_db: AsyncMock
    ) -> None:
        """Test incrementing token count."""
        mock_session = MagicMock()
        mock_session.token_count = 100
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_session
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        await repository.increment_token_count("session_123", 50)

        assert mock_session.token_count == 150

    @pytest.mark.asyncio
    async def test_delete_exists(
        self, repository: SessionRepository, mock_db: AsyncMock
    ) -> None:
        """Test deleting existing session."""
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_session
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.delete = AsyncMock()
        mock_db.commit = AsyncMock()

        result = await repository.delete("session_123")

        assert result is True
        mock_db.delete.assert_called_once_with(mock_session)

    @pytest.mark.asyncio
    async def test_delete_not_exists(
        self, repository: SessionRepository, mock_db: AsyncMock
    ) -> None:
        """Test deleting non-existent session."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.delete("nonexistent")

        assert result is False

    @pytest.mark.asyncio
    async def test_get_active_sessions(
        self, repository: SessionRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting active sessions."""
        mock_sessions = [MagicMock(), MagicMock()]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_sessions
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_active_sessions(limit=10)

        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_get_expired_sessions(
        self, repository: SessionRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting expired sessions."""
        mock_sessions = [MagicMock()]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_sessions
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_expired_sessions()

        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_cleanup_expired_sessions(
        self, repository: SessionRepository, mock_db: AsyncMock
    ) -> None:
        """Test cleaning up expired sessions."""
        mock_session1 = MagicMock()
        mock_session1.status = SessionStatus.ACTIVE
        mock_session2 = MagicMock()
        mock_session2.status = SessionStatus.ACTIVE

        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_session1, mock_session2]
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        count = await repository.cleanup_expired_sessions()

        assert count == 2
        assert mock_session1.status == SessionStatus.EXPIRED
        assert mock_session2.status == SessionStatus.EXPIRED
