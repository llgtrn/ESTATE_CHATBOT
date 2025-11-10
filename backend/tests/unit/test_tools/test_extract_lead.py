"""Tests for extract lead tool."""
from app.langchain.tools.extract_lead import ExtractLeadTool


class TestExtractLeadTool:
    """Tests for ExtractLeadTool class."""

    def test_init(self) -> None:
        """Test tool initialization."""
        tool = ExtractLeadTool()
        assert tool is not None

    def test_extract(self) -> None:
        """Test entity extraction."""
        tool = ExtractLeadTool()
        result = tool.extract("東京で2LDKのマンションを探しています")

        assert "entities" in result
        assert "confidence" in result
        assert isinstance(result["entities"], list)
        assert isinstance(result["confidence"], (int, float))

    def test_extract_empty_message(self) -> None:
        """Test extraction from empty message."""
        tool = ExtractLeadTool()
        result = tool.extract("")

        assert "entities" in result
        assert result["entities"] == []

    def test_validate_with_entities(self) -> None:
        """Test validation with entities."""
        tool = ExtractLeadTool()
        entities = {"location": "Tokyo", "budget": 5000000}

        assert tool.validate(entities)

    def test_validate_empty_entities(self) -> None:
        """Test validation with empty entities."""
        tool = ExtractLeadTool()
        assert not tool.validate({})

    def test_validate_none(self) -> None:
        """Test validation with None."""
        tool = ExtractLeadTool()
        assert not tool.validate(None)  # type: ignore
