"""Glossary search API endpoints."""
from typing import Any

from fastapi import APIRouter, Query

from app.api.dependencies import SettingsDep

router = APIRouter()


@router.get("/glossary/search")
async def search_glossary(
    query: str = Query(..., min_length=1, max_length=100),
    language: str = Query(default="ja", pattern="^(ja|en|vi)$"),
    settings: SettingsDep = None,
) -> dict[str, Any]:
    """Search glossary terms."""
    return {
        "query": query,
        "language": language,
        "results": [],
        "total": 0,
    }


@router.get("/glossary/terms/{term_id}")
async def get_term(term_id: str, settings: SettingsDep) -> dict[str, Any]:
    """Get glossary term details."""
    return {
        "term_id": term_id,
        "term": "築年数",
        "translation": "Building age",
        "explanation": "The age of the building from construction date",
        "language": "ja",
    }
