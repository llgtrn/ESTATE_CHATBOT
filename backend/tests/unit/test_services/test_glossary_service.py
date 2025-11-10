"""Tests for glossary service."""
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.services.glossary_service import GlossaryService


class TestGlossaryService:
    """Tests for GlossaryService class."""

    @pytest.fixture
    def mock_repo(self) -> AsyncMock:
        """Create mock glossary repository."""
        return AsyncMock()

    @pytest.fixture
    def service(self, mock_repo: AsyncMock) -> GlossaryService:
        """Create service instance."""
        return GlossaryService(mock_repo)

    @pytest.mark.asyncio
    async def test_search_terms(
        self, service: GlossaryService, mock_repo: AsyncMock
    ) -> None:
        """Test searching glossary terms."""
        mock_term = MagicMock()
        mock_term.id = "term_123"
        mock_term.term = "築年数"
        mock_term.translation = "Building Age"
        mock_term.explanation = "建物の年齢"
        mock_term.category = "property_info"
        mock_term.usage_count = 10

        mock_repo.search_by_term.return_value = [mock_term]

        result = await service.search_terms(query="築年数", language="ja")

        assert result["query"] == "築年数"
        assert result["language"] == "ja"
        assert len(result["results"]) == 1
        assert result["results"][0]["term"] == "築年数"
        assert result["total"] == 1

    @pytest.mark.asyncio
    async def test_search_terms_no_results(
        self, service: GlossaryService, mock_repo: AsyncMock
    ) -> None:
        """Test searching with no results."""
        mock_repo.search_by_term.return_value = []

        result = await service.search_terms(query="unknown", language="ja")

        assert result["total"] == 0
        assert result["results"] == []

    @pytest.mark.asyncio
    async def test_search_terms_multiple_results(
        self, service: GlossaryService, mock_repo: AsyncMock
    ) -> None:
        """Test searching with multiple results."""
        mock_terms = []
        for i in range(5):
            mock_term = MagicMock()
            mock_term.id = f"term_{i}"
            mock_term.term = f"Term {i}"
            mock_term.translation = f"Translation {i}"
            mock_term.explanation = f"Explanation {i}"
            mock_term.category = "test"
            mock_term.usage_count = i
            mock_terms.append(mock_term)

        mock_repo.search_by_term.return_value = mock_terms

        result = await service.search_terms(query="term", language="en", limit=10)

        assert result["total"] == 5
        assert len(result["results"]) == 5

    @pytest.mark.asyncio
    async def test_get_term(
        self, service: GlossaryService, mock_repo: AsyncMock
    ) -> None:
        """Test getting term details."""
        mock_term = MagicMock()
        mock_term.id = "term_123"
        mock_term.term = "敷金"
        mock_term.language = "ja"
        mock_term.translation = "Security Deposit"
        mock_term.explanation = "賃貸契約時に預けるお金"
        mock_term.category = "rental"
        mock_term.synonyms = ["保証金"]
        mock_term.examples = ["敷金2ヶ月"]
        mock_term.usage_count = 5

        mock_repo.get_by_id.return_value = mock_term
        mock_repo.increment_usage = AsyncMock()

        result = await service.get_term("term_123")

        assert result["term_id"] == "term_123"
        assert result["term"] == "敷金"
        assert result["usage_count"] == 6  # Incremented
        mock_repo.increment_usage.assert_called_once_with("term_123")

    @pytest.mark.asyncio
    async def test_get_term_not_found(
        self, service: GlossaryService, mock_repo: AsyncMock
    ) -> None:
        """Test getting non-existent term."""
        mock_repo.get_by_id.return_value = None

        result = await service.get_term("nonexistent")

        assert result == {}

    @pytest.mark.asyncio
    async def test_explain_term_found(
        self, service: GlossaryService, mock_repo: AsyncMock
    ) -> None:
        """Test explaining a term."""
        mock_term = MagicMock()
        mock_term.id = "term_123"
        mock_term.term = "礼金"
        mock_term.translation = "Key Money"
        mock_term.explanation = "賃貸契約時に支払うお礼のお金"
        mock_term.examples = ["礼金1ヶ月"]

        mock_repo.get_by_term.return_value = mock_term
        mock_repo.increment_usage = AsyncMock()

        result = await service.explain_term("礼金", language="ja")

        assert result is not None
        assert result["term"] == "礼金"
        assert result["translation"] == "Key Money"
        assert "examples" in result

    @pytest.mark.asyncio
    async def test_explain_term_not_found(
        self, service: GlossaryService, mock_repo: AsyncMock
    ) -> None:
        """Test explaining non-existent term."""
        mock_repo.get_by_term.return_value = None
        mock_repo.search_by_term.return_value = []

        result = await service.explain_term("unknown", language="ja")

        assert result is None

    @pytest.mark.asyncio
    async def test_explain_term_fallback_to_search(
        self, service: GlossaryService, mock_repo: AsyncMock
    ) -> None:
        """Test explaining term with fallback to search."""
        mock_term = MagicMock()
        mock_term.id = "term_123"
        mock_term.term = "駅近"
        mock_term.translation = "Near Station"
        mock_term.explanation = "駅から徒歩圏内"
        mock_term.examples = ["駅徒歩5分"]

        mock_repo.get_by_term.return_value = None
        mock_repo.search_by_term.return_value = [mock_term]
        mock_repo.increment_usage = AsyncMock()

        result = await service.explain_term("駅近", language="ja")

        assert result is not None
        assert result["term"] == "駅近"

    @pytest.mark.asyncio
    async def test_get_terms_by_category(
        self, service: GlossaryService, mock_repo: AsyncMock
    ) -> None:
        """Test getting terms by category."""
        mock_terms = []
        for i in range(3):
            mock_term = MagicMock()
            mock_term.id = f"term_{i}"
            mock_term.term = f"Term {i}"
            mock_term.translation = f"Translation {i}"
            mock_term.explanation = f"Explanation {i}"
            mock_terms.append(mock_term)

        mock_repo.get_by_category.return_value = mock_terms

        result = await service.get_terms_by_category(
            category="rental",
            language="ja",
        )

        assert len(result) == 3
        assert all("term_id" in term for term in result)

    @pytest.mark.asyncio
    async def test_get_terms_by_category_empty(
        self, service: GlossaryService, mock_repo: AsyncMock
    ) -> None:
        """Test getting terms by category with no results."""
        mock_repo.get_by_category.return_value = []

        result = await service.get_terms_by_category(
            category="nonexistent",
            language="ja",
        )

        assert result == []

    @pytest.mark.asyncio
    async def test_add_term(
        self, service: GlossaryService, mock_repo: AsyncMock
    ) -> None:
        """Test adding a new term."""
        mock_term = MagicMock()
        mock_term.id = "term_new"
        mock_term.term = "新用語"
        mock_term.language = "ja"
        mock_term.translation = "New Term"
        mock_term.explanation = "新しい用語"

        mock_repo.create.return_value = mock_term

        result = await service.add_term(
            term="新用語",
            language="ja",
            translation="New Term",
            explanation="新しい用語",
        )

        assert result["term_id"] == "term_new"
        assert result["term"] == "新用語"
        mock_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_term_with_extras(
        self, service: GlossaryService, mock_repo: AsyncMock
    ) -> None:
        """Test adding term with additional fields."""
        mock_term = MagicMock()
        mock_term.id = "term_new"
        mock_term.term = "Test"
        mock_term.language = "en"
        mock_term.translation = "テスト"
        mock_term.explanation = "Test term"

        mock_repo.create.return_value = mock_term

        result = await service.add_term(
            term="Test",
            language="en",
            translation="テスト",
            explanation="Test term",
            category="test",
            synonyms=["exam"],
        )

        assert result["term"] == "Test"
        mock_repo.create.assert_called_once()
