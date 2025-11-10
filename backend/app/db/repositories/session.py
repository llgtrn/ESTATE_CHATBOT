"""Session repository for database operations."""
import uuid
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Session, SessionStatus


class SessionRepository:
    """Repository for session operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize repository."""
        self.db = db

    async def create(
        self,
        language: str = "ja",
        user_id: str | None = None,
        metadata: dict[str, Any] | None = None,
        timeout_minutes: int = 60,
    ) -> Session:
        """Create a new session."""
        session_id = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(minutes=timeout_minutes)

        session = Session(
            id=session_id,
            status=SessionStatus.ACTIVE,
            language=language,
            user_id=user_id,
            metadata=metadata or {},
            expires_at=expires_at,
        )

        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)

        return session

    async def get_by_id(self, session_id: str) -> Session | None:
        """Get session by ID."""
        result = await self.db.execute(
            select(Session).where(Session.id == session_id)
        )
        return result.scalar_one_or_none()

    async def update(self, session: Session) -> Session:
        """Update session."""
        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def update_status(self, session_id: str, status: SessionStatus) -> Session | None:
        """Update session status."""
        session = await self.get_by_id(session_id)
        if session:
            session.status = status
            await self.update(session)
        return session

    async def increment_turn_count(self, session_id: str) -> None:
        """Increment turn count."""
        session = await self.get_by_id(session_id)
        if session:
            session.turn_count += 1
            await self.update(session)

    async def increment_token_count(self, session_id: str, tokens: int) -> None:
        """Increment token count."""
        session = await self.get_by_id(session_id)
        if session:
            session.token_count += tokens
            await self.update(session)

    async def delete(self, session_id: str) -> bool:
        """Delete session."""
        session = await self.get_by_id(session_id)
        if session:
            await self.db.delete(session)
            await self.db.commit()
            return True
        return False

    async def get_active_sessions(self, limit: int = 100) -> list[Session]:
        """Get active sessions."""
        result = await self.db.execute(
            select(Session)
            .where(Session.status == SessionStatus.ACTIVE)
            .order_by(Session.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_expired_sessions(self) -> list[Session]:
        """Get expired sessions."""
        now = datetime.utcnow()
        result = await self.db.execute(
            select(Session)
            .where(Session.status == SessionStatus.ACTIVE)
            .where(Session.expires_at < now)
        )
        return list(result.scalars().all())

    async def cleanup_expired_sessions(self) -> int:
        """Cleanup expired sessions."""
        expired_sessions = await self.get_expired_sessions()
        count = 0

        for session in expired_sessions:
            session.status = SessionStatus.EXPIRED
            await self.update(session)
            count += 1

        return count
