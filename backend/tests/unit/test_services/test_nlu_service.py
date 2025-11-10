"""Tests for NLU service."""
import pytest

from app.services.nlu_service import NLUService


class TestNLUService:
    """Tests for NLUService class."""

    def test_init(self) -> None:
        """Test service initialization."""
        service = NLUService()
        assert service is not None
        assert service.intent_patterns is not None
        assert service.entity_patterns is not None

    @pytest.mark.asyncio
    async def test_analyze_greeting_japanese(self) -> None:
        """Test analyzing Japanese greeting."""
        service = NLUService()
        result = await service.analyze("こんにちは", "ja")

        assert result["intent"] == "greeting"
        assert result["confidence"] > 0
        assert result["language"] == "ja"

    @pytest.mark.asyncio
    async def test_analyze_property_search_buy(self) -> None:
        """Test analyzing buy property intent."""
        service = NLUService()
        result = await service.analyze("マンションを買いたいです", "ja")

        assert result["intent"] == "property_search_buy"
        assert result["language"] == "ja"

    @pytest.mark.asyncio
    async def test_analyze_with_budget_entity(self) -> None:
        """Test extracting budget entity."""
        service = NLUService()
        result = await service.analyze("予算は5000万円です", "ja")

        assert "entities" in result
        assert "budget" in result["entities"]
        assert result["entities"]["budget"] == 50000000

    @pytest.mark.asyncio
    async def test_analyze_with_rooms_entity(self) -> None:
        """Test extracting rooms entity."""
        service = NLUService()
        result = await service.analyze("2LDKの物件を探しています", "ja")

        assert "entities" in result
        assert "rooms" in result["entities"]
        assert result["entities"]["rooms"] == "2LDK"

    @pytest.mark.asyncio
    async def test_analyze_with_location_entity(self) -> None:
        """Test extracting location entity."""
        service = NLUService()
        result = await service.analyze("東京で物件を探しています", "ja")

        assert "entities" in result
        assert "location" in result["entities"]
        assert result["entities"]["location"] == "東京"

    @pytest.mark.asyncio
    async def test_analyze_with_area_entity(self) -> None:
        """Test extracting area entity."""
        service = NLUService()
        result = await service.analyze("70㎡の物件がいいです", "ja")

        assert "entities" in result
        assert "area" in result["entities"]
        assert result["entities"]["area"] == 70.0

    @pytest.mark.asyncio
    async def test_analyze_no_intent(self) -> None:
        """Test analyzing text with no clear intent."""
        service = NLUService()
        result = await service.analyze("ランダムなテキスト", "ja")

        assert result["intent"] is None
        assert result["confidence"] == 0.0

    @pytest.mark.asyncio
    async def test_analyze_multiple_entities(self) -> None:
        """Test extracting multiple entities."""
        service = NLUService()
        result = await service.analyze(
            "東京で2LDKのマンションを5000万円で買いたいです", "ja"
        )

        entities = result["entities"]
        assert "location" in entities
        assert "rooms" in entities
        assert "budget" in entities
        assert entities["location"] == "東京"
        assert entities["rooms"] == "2LDK"
        assert entities["budget"] == 50000000

    def test_validate_entities_valid(self) -> None:
        """Test validating valid entities."""
        service = NLUService()
        entities = {"budget": 50000000, "area": 70.0}

        errors = service.validate_entities(entities)
        assert errors == []

    def test_validate_entities_invalid_budget(self) -> None:
        """Test validating invalid budget."""
        service = NLUService()
        entities = {"budget": -1000}

        errors = service.validate_entities(entities)
        assert len(errors) > 0
        assert "Budget must be positive" in errors

    def test_validate_entities_budget_too_high(self) -> None:
        """Test validating budget that's too high."""
        service = NLUService()
        entities = {"budget": 20000000000}  # 200億円

        errors = service.validate_entities(entities)
        assert len(errors) > 0
        assert "Budget is too high" in errors

    def test_validate_entities_invalid_area(self) -> None:
        """Test validating invalid area."""
        service = NLUService()
        entities = {"area": -10}

        errors = service.validate_entities(entities)
        assert len(errors) > 0
        assert "Area must be positive" in errors

    def test_validate_entities_area_too_large(self) -> None:
        """Test validating area that's too large."""
        service = NLUService()
        entities = {"area": 15000}

        errors = service.validate_entities(entities)
        assert len(errors) > 0
        assert "Area is too large" in errors

    @pytest.mark.asyncio
    async def test_analyze_english_greeting(self) -> None:
        """Test analyzing English greeting."""
        service = NLUService()
        result = await service.analyze("hello", "en")

        assert result["intent"] == "greeting"
        assert result["language"] == "en"

    @pytest.mark.asyncio
    async def test_analyze_vietnamese_greeting(self) -> None:
        """Test analyzing Vietnamese greeting."""
        service = NLUService()
        result = await service.analyze("xin chào", "vi")

        assert result["intent"] == "greeting"
        assert result["language"] == "vi"
