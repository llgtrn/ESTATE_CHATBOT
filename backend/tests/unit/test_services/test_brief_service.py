"""Tests for brief service."""
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.core.exceptions import BriefNotFoundError, ValidationError
from app.db.models import BriefStatus, PropertyType
from app.services.brief_service import BriefService


class TestBriefService:
    """Tests for BriefService class."""

    @pytest.fixture
    def mock_repo(self) -> AsyncMock:
        """Create mock brief repository."""
        return AsyncMock()

    @pytest.fixture
    def service(self, mock_repo: AsyncMock) -> BriefService:
        """Create service instance."""
        return BriefService(mock_repo)

    @pytest.mark.asyncio
    async def test_create_brief(
        self, service: BriefService, mock_repo: AsyncMock
    ) -> None:
        """Test creating a brief."""
        mock_brief = MagicMock()
        mock_brief.id = "brief_123"
        mock_brief.session_id = "session_123"
        mock_brief.property_type = PropertyType.BUY
        mock_brief.status = BriefStatus.DRAFT
        mock_brief.completeness_score = 0.0
        mock_brief.created_at.isoformat.return_value = "2025-01-01T00:00:00"
        mock_brief.updated_at.isoformat.return_value = "2025-01-01T00:00:00"
        mock_brief.submitted_at = None
        mock_brief.location = None
        mock_brief.budget_min = None
        mock_brief.budget_max = None
        mock_brief.rooms = None
        mock_brief.area_min = None
        mock_brief.area_max = None
        mock_brief.data = {}
        mock_brief.extracted_entities = {}
        mock_brief.lead_score = None

        mock_repo.create.return_value = mock_brief

        result = await service.create_brief(
            session_id="session_123",
            property_type=PropertyType.BUY,
        )

        assert result["brief_id"] == "brief_123"
        assert result["property_type"] == "buy"
        assert result["status"] == "draft"
        mock_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_brief(
        self, service: BriefService, mock_repo: AsyncMock
    ) -> None:
        """Test getting a brief."""
        mock_brief = MagicMock()
        mock_brief.id = "brief_123"
        mock_brief.property_type = PropertyType.BUY
        mock_brief.status = BriefStatus.DRAFT
        mock_brief.completeness_score = 50.0
        mock_brief.created_at.isoformat.return_value = "2025-01-01T00:00:00"
        mock_brief.updated_at.isoformat.return_value = "2025-01-01T00:00:00"
        mock_brief.submitted_at = None
        mock_brief.session_id = "session_123"
        mock_brief.location = "東京"
        mock_brief.budget_min = None
        mock_brief.budget_max = 50000000
        mock_brief.rooms = "2LDK"
        mock_brief.area_min = None
        mock_brief.area_max = None
        mock_brief.data = {}
        mock_brief.extracted_entities = {}
        mock_brief.lead_score = None

        mock_repo.get_by_id.return_value = mock_brief

        result = await service.get_brief("brief_123")

        assert result["brief_id"] == "brief_123"
        assert result["location"] == "東京"
        assert result["completeness_score"] == 50.0

    @pytest.mark.asyncio
    async def test_get_brief_not_found(
        self, service: BriefService, mock_repo: AsyncMock
    ) -> None:
        """Test getting non-existent brief."""
        mock_repo.get_by_id.return_value = None

        with pytest.raises(BriefNotFoundError):
            await service.get_brief("nonexistent")

    @pytest.mark.asyncio
    async def test_get_brief_by_session(
        self, service: BriefService, mock_repo: AsyncMock
    ) -> None:
        """Test getting brief by session."""
        mock_brief = MagicMock()
        mock_brief.id = "brief_123"
        mock_brief.session_id = "session_123"
        mock_brief.property_type = PropertyType.BUY
        mock_brief.status = BriefStatus.DRAFT
        mock_brief.completeness_score = 0.0
        mock_brief.created_at.isoformat.return_value = "2025-01-01T00:00:00"
        mock_brief.updated_at.isoformat.return_value = "2025-01-01T00:00:00"
        mock_brief.submitted_at = None
        mock_brief.location = None
        mock_brief.budget_min = None
        mock_brief.budget_max = None
        mock_brief.rooms = None
        mock_brief.area_min = None
        mock_brief.area_max = None
        mock_brief.data = {}
        mock_brief.extracted_entities = {}
        mock_brief.lead_score = None

        mock_repo.get_by_session.return_value = mock_brief

        result = await service.get_brief_by_session("session_123")

        assert result is not None
        assert result["session_id"] == "session_123"

    @pytest.mark.asyncio
    async def test_get_brief_by_session_not_found(
        self, service: BriefService, mock_repo: AsyncMock
    ) -> None:
        """Test getting brief by non-existent session."""
        mock_repo.get_by_session.return_value = None

        result = await service.get_brief_by_session("nonexistent")

        assert result is None

    @pytest.mark.asyncio
    async def test_update_brief(
        self, service: BriefService, mock_repo: AsyncMock
    ) -> None:
        """Test updating a brief."""
        mock_brief = MagicMock()
        mock_brief.id = "brief_123"
        mock_brief.property_type = PropertyType.BUY
        mock_brief.status = BriefStatus.DRAFT
        mock_brief.location = "東京"
        mock_brief.budget_max = 50000000
        mock_brief.rooms = "2LDK"
        mock_brief.data = {}
        mock_brief.completeness_score = 75.0
        mock_brief.created_at.isoformat.return_value = "2025-01-01T00:00:00"
        mock_brief.updated_at.isoformat.return_value = "2025-01-01T00:00:00"
        mock_brief.submitted_at = None
        mock_brief.session_id = "session_123"
        mock_brief.budget_min = None
        mock_brief.area_min = None
        mock_brief.area_max = None
        mock_brief.extracted_entities = {}
        mock_brief.lead_score = None

        mock_repo.get_by_id.return_value = mock_brief
        mock_repo.calculate_completeness.return_value = 75.0
        mock_repo.update.return_value = mock_brief

        result = await service.update_brief(
            brief_id="brief_123",
            location="大阪",
        )

        assert result["brief_id"] == "brief_123"
        mock_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_from_entities(
        self, service: BriefService, mock_repo: AsyncMock
    ) -> None:
        """Test updating brief from entities."""
        mock_brief = MagicMock()
        mock_brief.id = "brief_123"
        mock_brief.property_type = PropertyType.BUY
        mock_brief.status = BriefStatus.IN_PROGRESS
        mock_brief.location = None
        mock_brief.budget_max = None
        mock_brief.rooms = None
        mock_brief.extracted_entities = {}
        mock_brief.completeness_score = 0.0
        mock_brief.created_at.isoformat.return_value = "2025-01-01T00:00:00"
        mock_brief.updated_at.isoformat.return_value = "2025-01-01T00:00:00"
        mock_brief.submitted_at = None
        mock_brief.session_id = "session_123"
        mock_brief.budget_min = None
        mock_brief.area_min = None
        mock_brief.area_max = None
        mock_brief.data = {}
        mock_brief.lead_score = None

        mock_repo.get_by_id.return_value = mock_brief
        mock_repo.calculate_completeness.return_value = 50.0
        mock_repo.update.return_value = mock_brief

        entities = {
            "location": "東京",
            "budget": 50000000,
            "rooms": "2LDK",
        }

        result = await service.update_from_entities("brief_123", entities)

        assert result["brief_id"] == "brief_123"
        assert mock_brief.location == "東京"
        assert mock_brief.budget_max == 50000000
        assert mock_brief.rooms == "2LDK"

    @pytest.mark.asyncio
    async def test_submit_brief_success(
        self, service: BriefService, mock_repo: AsyncMock
    ) -> None:
        """Test submitting a valid brief."""
        mock_brief = MagicMock()
        mock_brief.id = "brief_123"
        mock_brief.property_type = PropertyType.BUY
        mock_brief.status = BriefStatus.DRAFT
        mock_brief.location = "東京"
        mock_brief.budget_max = 50000000
        mock_brief.budget_min = 30000000
        mock_brief.rooms = "2LDK"
        mock_brief.completeness_score = 100.0
        mock_brief.lead_score = 85.0
        mock_brief.created_at.isoformat.return_value = "2025-01-01T00:00:00"
        mock_brief.updated_at.isoformat.return_value = "2025-01-01T00:00:00"
        mock_brief.submitted_at.isoformat.return_value = "2025-01-01T01:00:00"
        mock_brief.session_id = "session_123"
        mock_brief.area_min = None
        mock_brief.area_max = None
        mock_brief.data = {}
        mock_brief.extracted_entities = {}

        mock_repo.get_by_id.return_value = mock_brief
        mock_repo.update_status.return_value = mock_brief

        result = await service.submit_brief("brief_123")

        assert result["status"] == "submitted"
        mock_repo.update_status.assert_called_once()

    @pytest.mark.asyncio
    async def test_submit_brief_validation_error(
        self, service: BriefService, mock_repo: AsyncMock
    ) -> None:
        """Test submitting invalid brief."""
        mock_brief = MagicMock()
        mock_brief.location = None  # Missing required field
        mock_brief.budget_max = None  # Missing required field
        mock_brief.budget_min = None
        mock_brief.rooms = None  # Missing required field

        mock_repo.get_by_id.return_value = mock_brief

        with pytest.raises(ValidationError):
            await service.submit_brief("brief_123")

    @pytest.mark.asyncio
    async def test_calculate_affordability(
        self, service: BriefService
    ) -> None:
        """Test affordability calculation."""
        result = await service.calculate_affordability(
            annual_income=10000000,  # 1000万円
            down_payment=20000000,   # 2000万円
            interest_rate=0.01,      # 1%
            loan_years=35,
        )

        assert result["annual_income"] == 10000000
        assert result["down_payment"] == 20000000
        assert result["max_loan_amount"] == 70000000  # 7x income
        assert result["max_affordable_price"] == 90000000  # loan + down payment
        assert "monthly_payment" in result
        assert result["interest_rate"] == 0.01
        assert result["loan_years"] == 35

    @pytest.mark.asyncio
    async def test_calculate_affordability_zero_interest(
        self, service: BriefService
    ) -> None:
        """Test affordability with zero interest rate."""
        result = await service.calculate_affordability(
            annual_income=10000000,
            down_payment=10000000,
            interest_rate=0.0,  # Zero interest
            loan_years=35,
        )

        assert result["max_loan_amount"] == 70000000
        assert result["monthly_payment"] > 0

    def test_validate_brief_valid(self, service: BriefService) -> None:
        """Test validating a valid brief."""
        mock_brief = MagicMock()
        mock_brief.location = "東京"
        mock_brief.budget_max = 50000000
        mock_brief.budget_min = 30000000
        mock_brief.rooms = "2LDK"

        errors = service._validate_brief(mock_brief)

        assert errors == []

    def test_validate_brief_missing_location(self, service: BriefService) -> None:
        """Test validating brief with missing location."""
        mock_brief = MagicMock()
        mock_brief.location = None
        mock_brief.budget_max = 50000000
        mock_brief.rooms = "2LDK"

        errors = service._validate_brief(mock_brief)

        assert "Location is required" in errors

    def test_validate_brief_missing_budget(self, service: BriefService) -> None:
        """Test validating brief with missing budget."""
        mock_brief = MagicMock()
        mock_brief.location = "東京"
        mock_brief.budget_max = None
        mock_brief.budget_min = None
        mock_brief.rooms = "2LDK"

        errors = service._validate_brief(mock_brief)

        assert "Budget is required" in errors

    def test_validate_brief_missing_rooms(self, service: BriefService) -> None:
        """Test validating brief with missing rooms."""
        mock_brief = MagicMock()
        mock_brief.location = "東京"
        mock_brief.budget_max = 50000000
        mock_brief.rooms = None

        errors = service._validate_brief(mock_brief)

        assert "Room configuration is required" in errors

    def test_calculate_lead_score_complete(self, service: BriefService) -> None:
        """Test lead score calculation for complete brief."""
        mock_brief = MagicMock()
        mock_brief.completeness_score = 100.0
        mock_brief.budget_min = 30000000
        mock_brief.budget_max = 50000000
        mock_brief.location = "東京"
        mock_brief.rooms = "2LDK"
        mock_brief.area_min = 70.0
        mock_brief.area_max = None

        score = service._calculate_lead_score(mock_brief)

        assert score == 100.0  # Maximum score

    def test_calculate_lead_score_partial(self, service: BriefService) -> None:
        """Test lead score calculation for partial brief."""
        mock_brief = MagicMock()
        mock_brief.completeness_score = 50.0
        mock_brief.budget_min = None
        mock_brief.budget_max = 50000000
        mock_brief.location = "東京"
        mock_brief.rooms = None
        mock_brief.area_min = None
        mock_brief.area_max = None

        score = service._calculate_lead_score(mock_brief)

        assert 0 < score < 100
