"""Tests for glossary repository."""
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.db.repositories.glossary import GlossaryRepository


class TestGlossaryRepository:
    """Tests for GlossaryRepository class."""

    @pytest.fixture
    def mock_db(self) -> AsyncMock:
        """Create mock database session."""
        return AsyncMock()

    @pytest.fixture
    def repository(self, mock_db: AsyncMock) -> GlossaryRepository:
        """Create repository instance."""
        return GlossaryRepository(mock_db)

    @pytest.mark.asyncio
    async def test_create_basic(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test creating a basic glossary term."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        term = await repository.create(
            term="築年数",
            language="ja",
            translation="Building Age",
            explanation="建物が建築されてから経過した年数",
        )

        assert term is not None
        assert term.term == "築年数"
        assert term.language == "ja"
        assert term.translation == "Building Age"
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_with_category(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test creating term with category."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        term = await repository.create(
            term="敷金",
            language="ja",
            translation="Security Deposit",
            explanation="賃貸契約時に預けるお金",
            category="rental",
        )

        assert term.category == "rental"

    @pytest.mark.asyncio
    async def test_create_with_synonyms(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test creating term with synonyms."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        synonyms = ["建築年数", "経過年数"]
        term = await repository.create(
            term="築年数",
            language="ja",
            translation="Building Age",
            explanation="説明",
            synonyms=synonyms,
        )

        assert term.synonyms == synonyms

    @pytest.mark.asyncio
    async def test_create_with_examples(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test creating term with examples."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        examples = ["築10年のマンション", "築浅物件"]
        term = await repository.create(
            term="築年数",
            language="ja",
            translation="Building Age",
            explanation="説明",
            examples=examples,
        )

        assert term.examples == examples

    @pytest.mark.asyncio
    async def test_create_with_embedding(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test creating term with embedding."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        embedding = [0.1, 0.2, 0.3]
        term = await repository.create(
            term="Test",
            language="ja",
            translation="Test",
            explanation="Test",
            embedding=embedding,
        )

        assert term.embedding == embedding

    @pytest.mark.asyncio
    async def test_create_with_metadata(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test creating term with metadata."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        metadata = {"source": "manual", "verified": True}
        term = await repository.create(
            term="Test",
            language="ja",
            translation="Test",
            explanation="Test",
            metadata=metadata,
        )

        assert term.metadata == metadata

    @pytest.mark.asyncio
    async def test_create_defaults_empty_lists_and_dict(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test that synonyms, examples, and metadata default to empty."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        term = await repository.create(
            term="Test",
            language="ja",
            translation="Test",
            explanation="Test",
        )

        assert term.synonyms == []
        assert term.examples == []
        assert term.metadata == {}

    @pytest.mark.asyncio
    async def test_get_by_id_exists(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting existing term by ID."""
        mock_term = MagicMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_term
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_id("term_123")

        assert result == mock_term
        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_id_not_exists(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting non-existent term."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_id("nonexistent")

        assert result is None

    @pytest.mark.asyncio
    async def test_get_by_term_exists(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting term by term name and language."""
        mock_term = MagicMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_term
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_term("築年数", "ja")

        assert result == mock_term

    @pytest.mark.asyncio
    async def test_get_by_term_not_exists(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting non-existent term by name."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_term("nonexistent", "ja")

        assert result is None

    @pytest.mark.asyncio
    async def test_get_by_term_different_language(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting term with different language."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)

        # Same term but different language should not match
        result = await repository.get_by_term("築年数", "en")

        assert result is None

    @pytest.mark.asyncio
    async def test_search_by_term_basic(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test searching terms."""
        mock_terms = [MagicMock(), MagicMock()]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_terms
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.search_by_term("築", language="ja")

        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_search_by_term_with_language(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test searching terms with specific language."""
        mock_terms = [MagicMock()]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_terms
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.search_by_term("security", language="en")

        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_search_by_term_with_limit(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test searching terms with custom limit."""
        mock_terms = [MagicMock() for _ in range(5)]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_terms
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.search_by_term("term", limit=5)

        assert len(result) == 5

    @pytest.mark.asyncio
    async def test_search_by_term_no_results(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test searching with no results."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.search_by_term("nonexistent")

        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_get_by_category_basic(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting terms by category."""
        mock_terms = [MagicMock(), MagicMock(), MagicMock()]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_terms
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_category("rental")

        assert len(result) == 3

    @pytest.mark.asyncio
    async def test_get_by_category_with_language(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting terms by category and language."""
        mock_terms = [MagicMock()]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_terms
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_category("rental", language="en")

        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_get_by_category_with_limit(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting terms by category with limit."""
        mock_terms = [MagicMock() for _ in range(50)]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_terms
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_category("property_info", limit=50)

        assert len(result) == 50

    @pytest.mark.asyncio
    async def test_get_by_category_empty(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting terms from empty category."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_category("nonexistent_category")

        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_get_all_no_filter(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting all terms without filter."""
        mock_terms = [MagicMock() for _ in range(100)]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_terms
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_all()

        assert len(result) == 100

    @pytest.mark.asyncio
    async def test_get_all_with_language(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting all terms for specific language."""
        mock_terms = [MagicMock() for _ in range(50)]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_terms
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_all(language="ja")

        assert len(result) == 50

    @pytest.mark.asyncio
    async def test_get_all_with_limit(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test getting all terms with custom limit."""
        mock_terms = [MagicMock() for _ in range(200)]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_terms
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_all(limit=200)

        assert len(result) == 200

    @pytest.mark.asyncio
    async def test_increment_usage_exists(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test incrementing usage count."""
        mock_term = MagicMock()
        mock_term.usage_count = 5
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_term
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.commit = AsyncMock()

        await repository.increment_usage("term_123")

        assert mock_term.usage_count == 6
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_increment_usage_not_exists(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test incrementing usage for non-existent term."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)

        # Should not raise error
        await repository.increment_usage("nonexistent")

    @pytest.mark.asyncio
    async def test_update(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test updating a glossary term."""
        mock_term = MagicMock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        result = await repository.update(mock_term)

        assert result == mock_term
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_embedding_exists(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test updating term embedding."""
        mock_term = MagicMock()
        mock_term.embedding = None
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_term
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        new_embedding = [0.5, 0.6, 0.7]
        result = await repository.update_embedding("term_123", new_embedding)

        assert mock_term.embedding == new_embedding
        assert result == mock_term

    @pytest.mark.asyncio
    async def test_update_embedding_not_exists(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test updating embedding for non-existent term."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.update_embedding("nonexistent", [0.1, 0.2])

        assert result is None

    @pytest.mark.asyncio
    async def test_delete_exists(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test deleting existing term."""
        mock_term = MagicMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_term
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.delete = AsyncMock()
        mock_db.commit = AsyncMock()

        result = await repository.delete("term_123")

        assert result is True
        mock_db.delete.assert_called_once_with(mock_term)

    @pytest.mark.asyncio
    async def test_delete_not_exists(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test deleting non-existent term."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await repository.delete("nonexistent")

        assert result is False

    @pytest.mark.asyncio
    async def test_semantic_search_placeholder(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test semantic search placeholder implementation."""
        query_embedding = [0.1, 0.2, 0.3]

        result = await repository.semantic_search(query_embedding)

        # Currently returns empty list as placeholder
        assert result == []

    @pytest.mark.asyncio
    async def test_semantic_search_with_language(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test semantic search with language parameter."""
        query_embedding = [0.1, 0.2, 0.3]

        result = await repository.semantic_search(query_embedding, language="en")

        assert result == []

    @pytest.mark.asyncio
    async def test_semantic_search_with_limit(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test semantic search with limit parameter."""
        query_embedding = [0.1, 0.2, 0.3]

        result = await repository.semantic_search(query_embedding, limit=5)

        assert result == []

    @pytest.mark.asyncio
    async def test_create_japanese_term(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test creating Japanese term."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        term = await repository.create(
            term="2LDK",
            language="ja",
            translation="2 Bedrooms + Living/Dining/Kitchen",
            explanation="リビング・ダイニング・キッチンと2つの部屋がある間取り",
            category="layout",
        )

        assert term.language == "ja"

    @pytest.mark.asyncio
    async def test_create_english_term(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test creating English term."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        term = await repository.create(
            term="Security Deposit",
            language="en",
            translation="敷金",
            explanation="Money paid to the landlord at the start of a tenancy",
            category="rental",
        )

        assert term.language == "en"

    @pytest.mark.asyncio
    async def test_create_vietnamese_term(
        self, repository: GlossaryRepository, mock_db: AsyncMock
    ) -> None:
        """Test creating Vietnamese term."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        term = await repository.create(
            term="Tiền đặt cọc",
            language="vi",
            translation="Security Deposit / 敷金",
            explanation="Số tiền trả cho chủ nhà khi bắt đầu thuê",
            category="rental",
        )

        assert term.language == "vi"
