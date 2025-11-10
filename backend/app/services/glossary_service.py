"""Glossary service for term search and explanation."""
import logging
from typing import Any

from app.db.repositories.glossary import GlossaryRepository

logger = logging.getLogger(__name__)


class GlossaryService:
    """Service for glossary operations."""

    def __init__(self, glossary_repo: GlossaryRepository) -> None:
        """Initialize service."""
        self.glossary_repo = glossary_repo

    async def search_terms(
        self,
        query: str,
        language: str = "ja",
        limit: int = 10,
    ) -> dict[str, Any]:
        """Search glossary terms."""
        logger.info(f"Searching glossary for: {query} in {language}")

        terms = await self.glossary_repo.search_by_term(
            query=query,
            language=language,
            limit=limit,
        )

        return {
            "query": query,
            "language": language,
            "results": [
                {
                    "term_id": term.id,
                    "term": term.term,
                    "translation": term.translation,
                    "explanation": term.explanation,
                    "category": term.category,
                    "usage_count": term.usage_count,
                }
                for term in terms
            ],
            "total": len(terms),
        }

    async def get_term(self, term_id: str) -> dict[str, Any]:
        """Get term details."""
        term = await self.glossary_repo.get_by_id(term_id)

        if not term:
            return {}

        # Increment usage count
        await self.glossary_repo.increment_usage(term_id)

        return {
            "term_id": term.id,
            "term": term.term,
            "language": term.language,
            "translation": term.translation,
            "explanation": term.explanation,
            "category": term.category,
            "synonyms": term.synonyms,
            "examples": term.examples,
            "usage_count": term.usage_count + 1,
        }

    async def explain_term(
        self,
        term: str,
        language: str = "ja",
    ) -> dict[str, Any] | None:
        """Explain a specific term."""
        logger.info(f"Explaining term: {term} in {language}")

        term_obj = await self.glossary_repo.get_by_term(
            term=term,
            language=language,
        )

        if not term_obj:
            # Try searching
            search_results = await self.glossary_repo.search_by_term(
                query=term,
                language=language,
                limit=1,
            )
            if search_results:
                term_obj = search_results[0]

        if not term_obj:
            return None

        # Increment usage
        await self.glossary_repo.increment_usage(term_obj.id)

        return {
            "term": term_obj.term,
            "translation": term_obj.translation,
            "explanation": term_obj.explanation,
            "examples": term_obj.examples,
        }

    async def get_terms_by_category(
        self,
        category: str,
        language: str = "ja",
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Get terms by category."""
        terms = await self.glossary_repo.get_by_category(
            category=category,
            language=language,
            limit=limit,
        )

        return [
            {
                "term_id": term.id,
                "term": term.term,
                "translation": term.translation,
                "explanation": term.explanation,
            }
            for term in terms
        ]

    async def add_term(
        self,
        term: str,
        language: str,
        translation: str,
        explanation: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Add a new glossary term."""
        logger.info(f"Adding new term: {term} in {language}")

        term_obj = await self.glossary_repo.create(
            term=term,
            language=language,
            translation=translation,
            explanation=explanation,
            **kwargs,
        )

        return {
            "term_id": term_obj.id,
            "term": term_obj.term,
            "language": term_obj.language,
            "translation": term_obj.translation,
            "explanation": term_obj.explanation,
        }
