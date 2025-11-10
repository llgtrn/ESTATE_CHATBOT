"""Brief service for managing property briefs."""
import logging
from typing import Any

from app.core.exceptions import BriefNotFoundError, ValidationError
from app.db.models import BriefStatus, PropertyType
from app.db.repositories.brief import BriefRepository

logger = logging.getLogger(__name__)


class BriefService:
    """Service for managing briefs."""

    def __init__(self, brief_repo: BriefRepository) -> None:
        """Initialize service."""
        self.brief_repo = brief_repo

    async def create_brief(
        self,
        session_id: str,
        property_type: PropertyType,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a new brief."""
        logger.info(f"Creating brief for session {session_id}, type: {property_type}")

        brief = await self.brief_repo.create(
            session_id=session_id,
            property_type=property_type,
            **kwargs,
        )

        return self._format_brief(brief)

    async def get_brief(self, brief_id: str) -> dict[str, Any]:
        """Get brief by ID."""
        brief = await self.brief_repo.get_by_id(brief_id)

        if not brief:
            raise BriefNotFoundError(brief_id)

        return self._format_brief(brief)

    async def get_brief_by_session(self, session_id: str) -> dict[str, Any] | None:
        """Get brief by session ID."""
        brief = await self.brief_repo.get_by_session(session_id)

        if not brief:
            return None

        return self._format_brief(brief)

    async def update_brief(
        self,
        brief_id: str,
        **updates: Any,
    ) -> dict[str, Any]:
        """Update brief."""
        brief = await self.brief_repo.get_by_id(brief_id)

        if not brief:
            raise BriefNotFoundError(brief_id)

        # Update fields
        for key, value in updates.items():
            if hasattr(brief, key) and value is not None:
                setattr(brief, key, value)

        # Update data dict
        if "data" in updates:
            brief.data.update(updates["data"])

        # Recalculate completeness
        completeness = await self.brief_repo.calculate_completeness(brief)
        brief.completeness_score = completeness

        updated_brief = await self.brief_repo.update(brief)

        return self._format_brief(updated_brief)

    async def update_from_entities(
        self,
        brief_id: str,
        entities: dict[str, Any],
    ) -> dict[str, Any]:
        """Update brief from extracted entities."""
        brief = await self.brief_repo.get_by_id(brief_id)

        if not brief:
            raise BriefNotFoundError(brief_id)

        # Map entities to brief fields
        field_mapping = {
            "location": "location",
            "budget": "budget_max",
            "rooms": "rooms",
            "area": "area_min",
        }

        for entity_key, brief_field in field_mapping.items():
            if entity_key in entities:
                setattr(brief, brief_field, entities[entity_key])

        # Store all extracted entities
        brief.extracted_entities.update(entities)

        # Recalculate completeness
        completeness = await self.brief_repo.calculate_completeness(brief)
        brief.completeness_score = completeness

        updated_brief = await self.brief_repo.update(brief)

        logger.info(
            f"Updated brief {brief_id} from entities, completeness: {completeness}%"
        )

        return self._format_brief(updated_brief)

    async def submit_brief(self, brief_id: str) -> dict[str, Any]:
        """Submit brief for processing."""
        brief = await self.brief_repo.get_by_id(brief_id)

        if not brief:
            raise BriefNotFoundError(brief_id)

        # Validate brief before submission
        validation_errors = self._validate_brief(brief)

        if validation_errors:
            raise ValidationError(
                "Brief validation failed",
                details={"errors": validation_errors},
            )

        # Calculate lead score
        lead_score = self._calculate_lead_score(brief)
        brief.lead_score = lead_score

        # Update status
        updated_brief = await self.brief_repo.update_status(
            brief_id, BriefStatus.SUBMITTED
        )

        logger.info(
            f"Brief {brief_id} submitted with lead score: {lead_score}"
        )

        return self._format_brief(updated_brief)

    def _validate_brief(self, brief: Any) -> list[str]:
        """Validate brief completeness."""
        errors = []

        if not brief.location:
            errors.append("Location is required")

        if not brief.budget_max and not brief.budget_min:
            errors.append("Budget is required")

        if not brief.rooms:
            errors.append("Room configuration is required")

        return errors

    def _calculate_lead_score(self, brief: Any) -> float:
        """Calculate lead quality score."""
        score = 0.0

        # Completeness (40 points)
        score += brief.completeness_score * 0.4

        # Budget range clarity (20 points)
        if brief.budget_min and brief.budget_max:
            score += 20

        # Location specificity (20 points)
        if brief.location:
            score += 20

        # Additional details (20 points)
        if brief.rooms:
            score += 10
        if brief.area_min or brief.area_max:
            score += 10

        return min(score, 100.0)

    def _format_brief(self, brief: Any) -> dict[str, Any]:
        """Format brief for API response."""
        return {
            "brief_id": brief.id,
            "session_id": brief.session_id,
            "property_type": brief.property_type.value,
            "status": brief.status.value,
            "location": brief.location,
            "budget_min": brief.budget_min,
            "budget_max": brief.budget_max,
            "rooms": brief.rooms,
            "area_min": brief.area_min,
            "area_max": brief.area_max,
            "data": brief.data,
            "extracted_entities": brief.extracted_entities,
            "completeness_score": brief.completeness_score,
            "lead_score": brief.lead_score,
            "created_at": brief.created_at.isoformat(),
            "updated_at": brief.updated_at.isoformat(),
            "submitted_at": brief.submitted_at.isoformat() if brief.submitted_at else None,
        }

    async def calculate_affordability(
        self,
        annual_income: float,
        down_payment: float,
        interest_rate: float = 0.01,  # 1% default
        loan_years: int = 35,
    ) -> dict[str, Any]:
        """Calculate affordability based on income and down payment."""
        # Calculate maximum loan amount based on income
        # Rule of thumb: 7x annual income
        max_loan = annual_income * 7

        # Calculate monthly payment
        monthly_rate = interest_rate / 12
        num_payments = loan_years * 12

        if monthly_rate > 0:
            monthly_payment = max_loan * (
                monthly_rate * (1 + monthly_rate) ** num_payments
            ) / ((1 + monthly_rate) ** num_payments - 1)
        else:
            monthly_payment = max_loan / num_payments

        # Maximum affordable price
        max_price = max_loan + down_payment

        return {
            "annual_income": annual_income,
            "down_payment": down_payment,
            "max_loan_amount": round(max_loan, 2),
            "max_affordable_price": round(max_price, 2),
            "monthly_payment": round(monthly_payment, 2),
            "interest_rate": interest_rate,
            "loan_years": loan_years,
        }
