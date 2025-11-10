"""Message repository for database operations."""
import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Message


class MessageRepository:
    """Repository for message operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize repository."""
        self.db = db

    async def create(
        self,
        session_id: str,
        role: str,
        content: str,
        language: str = "ja",
        intent: str | None = None,
        confidence: float | None = None,
        entities: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        token_count: int = 0,
    ) -> Message:
        """Create a new message."""
        message_id = str(uuid.uuid4())

        message = Message(
            id=message_id,
            session_id=session_id,
            role=role,
            content=content,
            language=language,
            intent=intent,
            confidence=confidence,
            entities=entities or {},
            metadata=metadata or {},
            token_count=token_count,
        )

        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)

        return message

    async def get_by_id(self, message_id: str) -> Message | None:
        """Get message by ID."""
        result = await self.db.execute(
            select(Message).where(Message.id == message_id)
        )
        return result.scalar_one_or_none()

    async def get_by_session(
        self,
        session_id: str,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[Message]:
        """Get messages by session ID."""
        query = (
            select(Message)
            .where(Message.session_id == session_id)
            .order_by(Message.created_at.asc())
            .offset(offset)
        )

        if limit is not None:
            query = query.limit(limit)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_recent_messages(
        self,
        session_id: str,
        count: int = 10,
    ) -> list[Message]:
        """Get recent messages for a session."""
        result = await self.db.execute(
            select(Message)
            .where(Message.session_id == session_id)
            .order_by(Message.created_at.desc())
            .limit(count)
        )
        messages = list(result.scalars().all())
        return list(reversed(messages))  # Return in chronological order

    async def count_by_session(self, session_id: str) -> int:
        """Count messages in a session."""
        result = await self.db.execute(
            select(Message)
            .where(Message.session_id == session_id)
        )
        return len(list(result.scalars().all()))

    async def get_by_intent(
        self,
        intent: str,
        limit: int = 100,
    ) -> list[Message]:
        """Get messages by intent."""
        result = await self.db.execute(
            select(Message)
            .where(Message.intent == intent)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def update(self, message: Message) -> Message:
        """Update message."""
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def delete(self, message_id: str) -> bool:
        """Delete message."""
        message = await self.get_by_id(message_id)
        if message:
            await self.db.delete(message)
            await self.db.commit()
            return True
        return False
