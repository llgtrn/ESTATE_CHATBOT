"""Brief management API endpoints."""
from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.api.dependencies import SettingsDep

router = APIRouter()


class BriefUpdate(BaseModel):
    """Brief update model."""

    status: str | None = None
    data: dict[str, Any] | None = None


@router.get("/briefs/{brief_id}")
async def get_brief(brief_id: str, settings: SettingsDep) -> dict[str, Any]:
    """Get brief details."""
    if not brief_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brief not found",
        )

    return {
        "brief_id": brief_id,
        "session_id": "session_123",
        "status": "draft",
        "property_type": "buy",
        "data": {},
        "created_at": "2025-01-01T00:00:00Z",
    }


@router.patch("/briefs/{brief_id}")
async def update_brief(
    brief_id: str,
    update: BriefUpdate,
    settings: SettingsDep,
) -> dict[str, Any]:
    """Update brief."""
    return {
        "brief_id": brief_id,
        "status": update.status or "draft",
        "updated_at": "2025-01-01T00:00:00Z",
    }


@router.post("/briefs/{brief_id}/submit")
async def submit_brief(brief_id: str, settings: SettingsDep) -> dict[str, Any]:
    """Submit brief for processing."""
    return {
        "brief_id": brief_id,
        "status": "submitted",
        "submitted_at": "2025-01-01T00:00:00Z",
    }
