"""Tests for database models."""
from datetime import datetime

import pytest

from app.db.models import (
    BriefStatus,
    PropertyType,
    SessionStatus,
)


class TestEnums:
    """Tests for model enums."""

    def test_property_type_enum(self) -> None:
        """Test PropertyType enum."""
        assert PropertyType.BUY.value == "buy"
        assert PropertyType.RENT.value == "rent"
        assert PropertyType.SELL.value == "sell"

    def test_session_status_enum(self) -> None:
        """Test SessionStatus enum."""
        assert SessionStatus.ACTIVE.value == "active"
        assert SessionStatus.COMPLETED.value == "completed"
        assert SessionStatus.EXPIRED.value == "expired"
        assert SessionStatus.ABANDONED.value == "abandoned"

    def test_brief_status_enum(self) -> None:
        """Test BriefStatus enum."""
        assert BriefStatus.DRAFT.value == "draft"
        assert BriefStatus.IN_PROGRESS.value == "in_progress"
        assert BriefStatus.COMPLETED.value == "completed"
        assert BriefStatus.SUBMITTED.value == "submitted"
