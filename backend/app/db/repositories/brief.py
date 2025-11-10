"""Brief repository for database operations."""
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Brief, BriefStatus, PropertyType


class BriefRepository:
    """Repository for brief operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize repository."""
        self.db = db

    async def create(
        self,
        session_id: str,
        property_type: PropertyType,
        status: BriefStatus = BriefStatus.DRAFT,
        **kwargs: Any,
    ) -> Brief:
        """Create a new brief."""
        brief_id = str(uuid.uuid4())

        brief = Brief(
            id=brief_id,
            session_id=session_id,
            property_type=property_type,
            status=status,
            **kwargs,
        )

        self.db.add(brief)
        await self.db.commit()
        await self.db.refresh(brief)

        return brief

    async def get_by_id(self, brief_id: str) -> Brief | None:
        """Get brief by ID."""
        result = await self.db.execute(
            select(Brief).where(Brief.id == brief_id)
        )
        return result.scalar_one_or_none()

    async def get_by_session(self, session_id: str) -> Brief | None:
        """Get brief by session ID."""
        result = await self.db.execute(
            select(Brief).where(Brief.session_id == session_id)
        )
        return result.scalar_one_or_none()

    async def update(self, brief: Brief) -> Brief:
        """Update brief."""
        await self.db.commit()
        await self.db.refresh(brief)
        return brief

    async def update_status(self, brief_id: str, status: BriefStatus) -> Brief | None:
        """Update brief status."""
        brief = await self.get_by_id(brief_id)
        if brief:
            brief.status = status
            if status == BriefStatus.SUBMITTED:
                brief.submitted_at = datetime.utcnow()
            await self.update(brief)
        return brief

    async def update_data(
        self,
        brief_id: str,
        data: dict[str, Any],
    ) -> Brief | None:
        """Update brief data."""
        brief = await self.get_by_id(brief_id)
        if brief:
            brief.data.update(data)
            await self.update(brief)
        return brief

    async def update_entities(
        self,
        brief_id: str,
        entities: dict[str, Any],
    ) -> Brief | None:
        """Update extracted entities."""
        brief = await self.get_by_id(brief_id)
        if brief:
            brief.extracted_entities.update(entities)
            await self.update(brief)
        return brief

    async def update_completeness_score(
        self,
        brief_id: str,
        score: float,
    ) -> Brief | None:
        """Update completeness score."""
        brief = await self.get_by_id(brief_id)
        if brief:
            brief.completeness_score = score
            await self.update(brief)
        return brief

    async def get_by_property_type(
        self,
        property_type: PropertyType,
        limit: int = 100,
    ) -> list[Brief]:
        """Get briefs by property type."""
        result = await self.db.execute(
            select(Brief)
            .where(Brief.property_type == property_type)
            .order_by(Brief.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_status(
        self,
        status: BriefStatus,
        limit: int = 100,
    ) -> list[Brief]:
        """Get briefs by status."""
        result = await self.db.execute(
            select(Brief)
            .where(Brief.status == status)
            .order_by(Brief.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_submitted_briefs(
        self,
        limit: int = 100,
    ) -> list[Brief]:
        """Get submitted briefs."""
        return await self.get_by_status(BriefStatus.SUBMITTED, limit)

    async def delete(self, brief_id: str) -> bool:
        """Delete brief."""
        brief = await self.get_by_id(brief_id)
        if brief:
            await self.db.delete(brief)
            await self.db.commit()
            return True
        return False

    async def calculate_completeness(self, brief: Brief) -> float:
        """Calculate brief completeness score."""
        required_fields = ["location", "budget_min", "budget_max", "rooms"]
        filled_fields = 0

        for field in required_fields:
            value = getattr(brief, field, None)
            if value is not None:
                filled_fields += 1

        score = (filled_fields / len(required_fields)) * 100
        return round(score, 2)
