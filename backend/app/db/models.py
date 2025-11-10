"""SQLAlchemy database models."""
import enum
from datetime import datetime
from typing import Any

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector


class Base(DeclarativeBase):
    """Base model class."""

    pass


class PropertyType(str, enum.Enum):
    """Property type enumeration."""

    BUY = "buy"
    RENT = "rent"
    SELL = "sell"


class SessionStatus(str, enum.Enum):
    """Session status enumeration."""

    ACTIVE = "active"
    COMPLETED = "completed"
    EXPIRED = "expired"
    ABANDONED = "abandoned"


class BriefStatus(str, enum.Enum):
    """Brief status enumeration."""

    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SUBMITTED = "submitted"


class Session(Base):
    """Conversation session model."""

    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, index=True)
    status: Mapped[SessionStatus] = mapped_column(
        Enum(SessionStatus), default=SessionStatus.ACTIVE, index=True
    )
    language: Mapped[str] = mapped_column(String(5), default="ja")
    user_id: Mapped[str | None] = mapped_column(String(255), index=True, nullable=True)
    metadata: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    turn_count: Mapped[int] = mapped_column(Integer, default=0)
    token_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
    expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationships
    messages: Mapped[list["Message"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )
    brief: Mapped["Brief | None"] = relationship(back_populates="session", uselist=False)

    __table_args__ = (
        Index("ix_sessions_status_created", "status", "created_at"),
        Index("ix_sessions_user_status", "user_id", "status"),
    )


class Message(Base):
    """Conversation message model."""

    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, index=True)
    session_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("sessions.id", ondelete="CASCADE"), index=True
    )
    role: Mapped[str] = mapped_column(String(20))  # user, assistant, system
    content: Mapped[str] = mapped_column(Text)
    language: Mapped[str] = mapped_column(String(5), default="ja")
    intent: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    entities: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    metadata: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    token_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    session: Mapped[Session] = relationship(back_populates="messages")

    __table_args__ = (
        Index("ix_messages_session_created", "session_id", "created_at"),
        Index("ix_messages_intent", "intent"),
    )


class Brief(Base):
    """Property brief model."""

    __tablename__ = "briefs"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, index=True)
    session_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("sessions.id", ondelete="CASCADE"), unique=True
    )
    property_type: Mapped[PropertyType] = mapped_column(
        Enum(PropertyType), index=True
    )
    status: Mapped[BriefStatus] = mapped_column(
        Enum(BriefStatus), default=BriefStatus.DRAFT, index=True
    )

    # Core fields
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    budget_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    budget_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    rooms: Mapped[str | None] = mapped_column(String(50), nullable=True)
    area_min: Mapped[float | None] = mapped_column(Float, nullable=True)
    area_max: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Additional data
    data: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    extracted_entities: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    validation_errors: Mapped[list[str]] = mapped_column(JSON, default=list)
    completeness_score: Mapped[float] = mapped_column(Float, default=0.0)
    lead_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationships
    session: Mapped[Session] = relationship(back_populates="brief")

    __table_args__ = (
        Index("ix_briefs_property_type_status", "property_type", "status"),
        Index("ix_briefs_created", "created_at"),
    )


class GlossaryTerm(Base):
    """Glossary term model."""

    __tablename__ = "glossary_terms"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, index=True)
    term: Mapped[str] = mapped_column(String(255), index=True)
    language: Mapped[str] = mapped_column(String(5), index=True)
    translation: Mapped[str] = mapped_column(String(255))
    explanation: Mapped[str] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    synonyms: Mapped[list[str]] = mapped_column(JSON, default=list)
    examples: Mapped[list[str]] = mapped_column(JSON, default=list)
    embedding: Mapped[Any] = mapped_column(Vector(768), nullable=True)
    metadata: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    usage_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        Index("ix_glossary_term_language", "term", "language", unique=True),
        Index("ix_glossary_embedding", "embedding", postgresql_using="ivfflat"),
    )


class ConversationMemory(Base):
    """Conversation memory for context management."""

    __tablename__ = "conversation_memory"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, index=True)
    session_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("sessions.id", ondelete="CASCADE"), index=True
    )
    memory_type: Mapped[str] = mapped_column(String(50), index=True)  # buffer, summary, entity
    content: Mapped[str] = mapped_column(Text)
    metadata: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        Index("ix_memory_session_type", "session_id", "memory_type"),
    )


class Analytics(Base):
    """Analytics and metrics model."""

    __tablename__ = "analytics"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, index=True)
    session_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False), nullable=True, index=True
    )
    event_type: Mapped[str] = mapped_column(String(100), index=True)
    event_data: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    token_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cost_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)

    __table_args__ = (
        Index("ix_analytics_event_type_created", "event_type", "created_at"),
        Index("ix_analytics_session", "session_id"),
    )
