"""Initial schema creation

Revision ID: 001
Revises:
Create Date: 2025-01-10 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create initial database schema."""
    # Enable pgvector extension
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # Create sessions table
    op.create_table(
        "sessions",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("ACTIVE", "COMPLETED", "EXPIRED", "ABANDONED", name="sessionstatus"),
            nullable=False,
        ),
        sa.Column("language", sa.String(5), nullable=False),
        sa.Column("user_id", sa.String(255), nullable=True),
        sa.Column("metadata", postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column("turn_count", sa.Integer(), nullable=False),
        sa.Column("token_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_sessions_id", "sessions", ["id"])
    op.create_index("ix_sessions_status", "sessions", ["status"])
    op.create_index("ix_sessions_status_created", "sessions", ["status", "created_at"])
    op.create_index("ix_sessions_user_status", "sessions", ["user_id", "status"])

    # Create messages table
    op.create_table(
        "messages",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("session_id", sa.String(), nullable=False),
        sa.Column("role", sa.String(20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("language", sa.String(5), nullable=False),
        sa.Column("intent", sa.String(100), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("entities", postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column("metadata", postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column("token_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_messages_id", "messages", ["id"])
    op.create_index("ix_messages_session_id", "messages", ["session_id"])
    op.create_index("ix_messages_session_created", "messages", ["session_id", "created_at"])
    op.create_index("ix_messages_intent", "messages", ["intent"])

    # Create briefs table
    op.create_table(
        "briefs",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("session_id", sa.String(), nullable=False),
        sa.Column(
            "property_type",
            sa.Enum("BUY", "RENT", "SELL", name="propertytype"),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.Enum("DRAFT", "IN_PROGRESS", "COMPLETED", "SUBMITTED", name="briefstatus"),
            nullable=False,
        ),
        sa.Column("location", sa.String(255), nullable=True),
        sa.Column("budget_min", sa.Integer(), nullable=True),
        sa.Column("budget_max", sa.Integer(), nullable=True),
        sa.Column("rooms", sa.String(50), nullable=True),
        sa.Column("area_min", sa.Float(), nullable=True),
        sa.Column("area_max", sa.Float(), nullable=True),
        sa.Column("data", postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column("extracted_entities", postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column("validation_errors", postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column("completeness_score", sa.Float(), nullable=False),
        sa.Column("lead_score", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("submitted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["session_id"], ["sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("session_id"),
    )
    op.create_index("ix_briefs_id", "briefs", ["id"])
    op.create_index("ix_briefs_property_type_status", "briefs", ["property_type", "status"])
    op.create_index("ix_briefs_created", "briefs", ["created_at"])

    # Create glossary_terms table
    op.create_table(
        "glossary_terms",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("term", sa.String(255), nullable=False),
        sa.Column("language", sa.String(5), nullable=False),
        sa.Column("translation", sa.String(255), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("category", sa.String(100), nullable=True),
        sa.Column("synonyms", postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column("examples", postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column("embedding", postgresql.ARRAY(sa.Float()), nullable=True),
        sa.Column("metadata", postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column("usage_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_glossary_terms_id", "glossary_terms", ["id"])
    op.create_index("ix_glossary_term_language", "glossary_terms", ["term", "language"], unique=True)
    op.create_index("ix_glossary_category", "glossary_terms", ["category"])

    # Create conversation_memory table
    op.create_table(
        "conversation_memory",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("session_id", sa.String(), nullable=False),
        sa.Column("memory_type", sa.String(50), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("metadata", postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_memory_id", "conversation_memory", ["id"])
    op.create_index("ix_memory_session_type", "conversation_memory", ["session_id", "memory_type"])

    # Create analytics table
    op.create_table(
        "analytics",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("session_id", sa.String(), nullable=True),
        sa.Column("event_type", sa.String(100), nullable=False),
        sa.Column("event_data", postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("token_count", sa.Integer(), nullable=True),
        sa.Column("cost_usd", sa.Float(), nullable=True),
        sa.Column("model", sa.String(100), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_analytics_id", "analytics", ["id"])
    op.create_index("ix_analytics_event_type_created", "analytics", ["event_type", "created_at"])
    op.create_index("ix_analytics_session", "analytics", ["session_id"])
    op.create_index("ix_analytics_created", "analytics", ["created_at"])


def downgrade() -> None:
    """Drop all tables and extensions."""
    op.drop_table("analytics")
    op.drop_table("conversation_memory")
    op.drop_table("glossary_terms")
    op.drop_table("briefs")
    op.drop_table("messages")
    op.drop_table("sessions")

    op.execute("DROP TYPE IF EXISTS sessionstatus")
    op.execute("DROP TYPE IF EXISTS propertytype")
    op.execute("DROP TYPE IF EXISTS briefstatus")
    op.execute("DROP EXTENSION IF EXISTS vector")
