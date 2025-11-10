"""Tests for brief repository."""
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.db.models import BriefStatus, PropertyType
from app.db.repositories.brief import BriefRepository


class TestBriefRepository:
    """Tests for BriefRepository class."""

    @pytest.fixture
    def mock_db(self) -> AsyncMock:
        """Create mock database session."""
        return AsyncMock()

    @pytest.fixture
    def repository(self, mock_db: AsyncMock) -> BriefRepository:
        """Create repository instance."""
        return BriefRepository(mock_db)

    @pytest.mark.asyncio
    async def test_create_basic(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test creating a basic brief."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        brief = await repository.create(
            session_id="session_123",
            property_type=PropertyType.BUY,
        )

        assert brief is not None
        assert brief.session_id == "session_123"
        assert brief.property_type == PropertyType.BUY
        assert brief.status == BriefStatus.DRAFT
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_with_status(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test creating brief with specific status."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        brief = await repository.create(
            session_id="session_123",
            property_type=PropertyType.RENT,
            status=BriefStatus.IN_PROGRESS,
        )

        assert brief.status == BriefStatus.IN_PROGRESS

    @pytest.mark.asyncio
    async def test_create_with_kwargs(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test creating brief with additional kwargs."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        brief = await repository.create(
            session_id="session_123",
            property_type=PropertyType.BUY,
            location="東京都渋谷区",
            budget_min=50000000,
            budget_max=80000000,
            rooms="3LDK",
        )

        assert brief.location == "東京都渋谷区"
        assert brief.budget_min == 50000000
        assert brief.budget_max == 80000000
        assert brief.rooms == "3LDK"

    @pytest.mark.asyncio
    async def test_create_buy_brief(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test creating a buy property brief."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        brief = await repository.create(
            session_id="session_123",
            property_type=PropertyType.BUY,
            location="東京",
            budget_min=60000000,
            budget_max=90000000,
        )

        assert brief.property_type == PropertyType.BUY

    @pytest.mark.asyncio
    async def test_create_rent_brief(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test creating a rent property brief."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        brief = await repository.create(
            session_id="session_123",
            property_type=PropertyType.RENT,
            location="大阪",
            budget_min=100000,
            budget_max=150000,
        )

        assert brief.property_type == PropertyType.RENT

    @pytest.mark.asyncio
    async def test_create_sell_brief(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test creating a sell property brief."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        brief = await repository.create(
            session_id="session_123",
            property_type=PropertyType.SELL,
            location="横浜",
            asking_price=75000000,
        )

        assert brief.property_type == PropertyType.SELL

    @pytest.mark.asyncio
    async def test_get_by_id_exists(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting existing brief by ID."""
        mock_brief = MagicMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_brief
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_id("brief_123")

        assert result == mock_brief
        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_id_not_exists(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting non-existent brief."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_id("nonexistent")

        assert result is None

    @pytest.mark.asyncio
    async def test_get_by_session_exists(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting brief by session ID."""
        mock_brief = MagicMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_brief
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_session("session_123")

        assert result == mock_brief

    @pytest.mark.asyncio
    async def test_get_by_session_not_exists(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting brief by non-existent session."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_session("nonexistent")

        assert result is None

    @pytest.mark.asyncio
    async def test_update(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test updating a brief."""
        mock_brief = MagicMock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        result = await repository.update(mock_brief)

        assert result == mock_brief
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_status_to_submitted(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test updating brief status to submitted."""
        mock_brief = MagicMock()
        mock_brief.status = BriefStatus.DRAFT
        mock_brief.submitted_at = None
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_brief
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        result = await repository.update_status("brief_123", BriefStatus.SUBMITTED)

        assert mock_brief.status == BriefStatus.SUBMITTED
        assert mock_brief.submitted_at is not None

    @pytest.mark.asyncio
    async def test_update_status_to_in_progress(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test updating brief status to in progress."""
        mock_brief = MagicMock()
        mock_brief.status = BriefStatus.DRAFT
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_brief
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        result = await repository.update_status("brief_123", BriefStatus.IN_PROGRESS)

        assert mock_brief.status == BriefStatus.IN_PROGRESS

    @pytest.mark.asyncio
    async def test_update_status_not_found(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test updating status for non-existent brief."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.update_status("nonexistent", BriefStatus.SUBMITTED)

        assert result is None

    @pytest.mark.asyncio
    async def test_update_data(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test updating brief data."""
        mock_brief = MagicMock()
        mock_brief.data = {"key1": "value1"}
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_brief
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        new_data = {"key2": "value2", "key3": "value3"}
        await repository.update_data("brief_123", new_data)

        mock_brief.data.update.assert_called_once_with(new_data)

    @pytest.mark.asyncio
    async def test_update_data_not_found(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test updating data for non-existent brief."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.update_data("nonexistent", {"key": "value"})

        assert result is None

    @pytest.mark.asyncio
    async def test_update_entities(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test updating extracted entities."""
        mock_brief = MagicMock()
        mock_brief.extracted_entities = {"budget": 50000000}
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_brief
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        new_entities = {"rooms": "3LDK", "location": "東京"}
        await repository.update_entities("brief_123", new_entities)

        mock_brief.extracted_entities.update.assert_called_once_with(new_entities)

    @pytest.mark.asyncio
    async def test_update_entities_not_found(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test updating entities for non-existent brief."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.update_entities("nonexistent", {"key": "value"})

        assert result is None

    @pytest.mark.asyncio
    async def test_update_completeness_score(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test updating completeness score."""
        mock_brief = MagicMock()
        mock_brief.completeness_score = 0.0
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_brief
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        result = await repository.update_completeness_score("brief_123", 75.5)

        assert mock_brief.completeness_score == 75.5

    @pytest.mark.asyncio
    async def test_update_completeness_score_not_found(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test updating score for non-existent brief."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.update_completeness_score("nonexistent", 50.0)

        assert result is None

    @pytest.mark.asyncio
    async def test_get_by_property_type_buy(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting briefs by buy property type."""
        mock_briefs = [MagicMock(), MagicMock()]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_briefs
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_property_type(PropertyType.BUY)

        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_get_by_property_type_rent(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting briefs by rent property type."""
        mock_briefs = [MagicMock()]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_briefs
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_property_type(PropertyType.RENT)

        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_get_by_property_type_with_limit(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting briefs with custom limit."""
        mock_briefs = [MagicMock() for _ in range(50)]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_briefs
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_property_type(PropertyType.BUY, limit=50)

        assert len(result) == 50

    @pytest.mark.asyncio
    async def test_get_by_property_type_empty(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting briefs with no results."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_property_type(PropertyType.SELL)

        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_get_by_status_draft(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting briefs by draft status."""
        mock_briefs = [MagicMock(), MagicMock(), MagicMock()]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_briefs
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_status(BriefStatus.DRAFT)

        assert len(result) == 3

    @pytest.mark.asyncio
    async def test_get_by_status_submitted(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting briefs by submitted status."""
        mock_briefs = [MagicMock()]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_briefs
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_status(BriefStatus.SUBMITTED)

        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_get_by_status_with_limit(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting briefs by status with limit."""
        mock_briefs = [MagicMock() for _ in range(20)]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_briefs
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_status(BriefStatus.IN_PROGRESS, limit=20)

        assert len(result) == 20

    @pytest.mark.asyncio
    async def test_get_submitted_briefs(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting submitted briefs."""
        mock_briefs = [MagicMock(), MagicMock()]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_briefs
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_submitted_briefs()

        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_get_submitted_briefs_with_limit(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting submitted briefs with limit."""
        mock_briefs = [MagicMock() for _ in range(30)]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_briefs
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_submitted_briefs(limit=30)

        assert len(result) == 30

    @pytest.mark.asyncio
    async def test_delete_exists(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test deleting existing brief."""
        mock_brief = MagicMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_brief
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.delete = AsyncMock()
        mock_db.commit = AsyncMock()

        result = await repository.delete("brief_123")

        assert result is True
        mock_db.delete.assert_called_once_with(mock_brief)

    @pytest.mark.asyncio
    async def test_delete_not_exists(
        self, repository: BriefRepository, mock_db: AsyncMock
    ) -> None:
        """Test deleting non-existent brief."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.delete("nonexistent")

        assert result is False

    @pytest.mark.asyncio
    async def test_calculate_completeness_empty(
        self, repository: BriefRepository
    ) -> None:
        """Test calculating completeness for empty brief."""
        mock_brief = MagicMock()
        mock_brief.location = None
        mock_brief.budget_min = None
        mock_brief.budget_max = None
        mock_brief.rooms = None

        score = await repository.calculate_completeness(mock_brief)

        assert score == 0.0

    @pytest.mark.asyncio
    async def test_calculate_completeness_partial(
        self, repository: BriefRepository
    ) -> None:
        """Test calculating completeness for partially filled brief."""
        mock_brief = MagicMock()
        mock_brief.location = "東京"
        mock_brief.budget_min = 50000000
        mock_brief.budget_max = None
        mock_brief.rooms = None

        score = await repository.calculate_completeness(mock_brief)

        assert score == 50.0  # 2 out of 4 fields

    @pytest.mark.asyncio
    async def test_calculate_completeness_full(
        self, repository: BriefRepository
    ) -> None:
        """Test calculating completeness for fully filled brief."""
        mock_brief = MagicMock()
        mock_brief.location = "東京都渋谷区"
        mock_brief.budget_min = 50000000
        mock_brief.budget_max = 80000000
        mock_brief.rooms = "3LDK"

        score = await repository.calculate_completeness(mock_brief)

        assert score == 100.0

    @pytest.mark.asyncio
    async def test_calculate_completeness_three_quarters(
        self, repository: BriefRepository
    ) -> None:
        """Test calculating completeness for 75% filled brief."""
        mock_brief = MagicMock()
        mock_brief.location = "横浜"
        mock_brief.budget_min = 40000000
        mock_brief.budget_max = 60000000
        mock_brief.rooms = None

        score = await repository.calculate_completeness(mock_brief)

        assert score == 75.0  # 3 out of 4 fields
