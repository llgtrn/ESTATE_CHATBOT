"""Glossary repository for database operations."""
import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import GlossaryTerm


class GlossaryRepository:
    """Repository for glossary operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize repository."""
        self.db = db

    async def create(
        self,
        term: str,
        language: str,
        translation: str,
        explanation: str,
        category: str | None = None,
        synonyms: list[str] | None = None,
        examples: list[str] | None = None,
        embedding: Any = None,
        metadata: dict[str, Any] | None = None,
    ) -> GlossaryTerm:
        """Create a new glossary term."""
        term_id = str(uuid.uuid4())

        glossary_term = GlossaryTerm(
            id=term_id,
            term=term,
            language=language,
            translation=translation,
            explanation=explanation,
            category=category,
            synonyms=synonyms or [],
            examples=examples or [],
            embedding=embedding,
            metadata=metadata or {},
        )

        self.db.add(glossary_term)
        await self.db.commit()
        await self.db.refresh(glossary_term)

        return glossary_term

    async def get_by_id(self, term_id: str) -> GlossaryTerm | None:
        """Get glossary term by ID."""
        result = await self.db.execute(
            select(GlossaryTerm).where(GlossaryTerm.id == term_id)
        )
        return result.scalar_one_or_none()

    async def get_by_term(self, term: str, language: str) -> GlossaryTerm | None:
        """Get glossary term by term and language."""
        result = await self.db.execute(
            select(GlossaryTerm)
            .where(GlossaryTerm.term == term)
            .where(GlossaryTerm.language == language)
        )
        return result.scalar_one_or_none()

    async def search_by_term(
        self,
        query: str,
        language: str = "ja",
        limit: int = 10,
    ) -> list[GlossaryTerm]:
        """Search glossary terms."""
        result = await self.db.execute(
            select(GlossaryTerm)
            .where(GlossaryTerm.language == language)
            .where(GlossaryTerm.term.ilike(f"%{query}%"))
            .order_by(GlossaryTerm.usage_count.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_category(
        self,
        category: str,
        language: str = "ja",
        limit: int = 100,
    ) -> list[GlossaryTerm]:
        """Get glossary terms by category."""
        result = await self.db.execute(
            select(GlossaryTerm)
            .where(GlossaryTerm.category == category)
            .where(GlossaryTerm.language == language)
            .order_by(GlossaryTerm.term.asc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_all(
        self,
        language: str | None = None,
        limit: int = 1000,
    ) -> list[GlossaryTerm]:
        """Get all glossary terms."""
        query = select(GlossaryTerm).order_by(GlossaryTerm.term.asc()).limit(limit)

        if language:
            query = query.where(GlossaryTerm.language == language)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def increment_usage(self, term_id: str) -> None:
        """Increment usage count."""
        term = await self.get_by_id(term_id)
        if term:
            term.usage_count += 1
            await self.db.commit()

    async def update(self, term: GlossaryTerm) -> GlossaryTerm:
        """Update glossary term."""
        await self.db.commit()
        await self.db.refresh(term)
        return term

    async def update_embedding(
        self,
        term_id: str,
        embedding: Any,
    ) -> GlossaryTerm | None:
        """Update term embedding."""
        term = await self.get_by_id(term_id)
        if term:
            term.embedding = embedding
            await self.update(term)
        return term

    async def delete(self, term_id: str) -> bool:
        """Delete glossary term."""
        term = await self.get_by_id(term_id)
        if term:
            await self.db.delete(term)
            await self.db.commit()
            return True
        return False

    async def semantic_search(
        self,
        query_embedding: Any,
        language: str = "ja",
        limit: int = 10,
    ) -> list[GlossaryTerm]:
        """Semantic search using vector similarity."""
        # This requires pgvector extension
        # For now, return empty list (will implement with actual vector search)
        return []
