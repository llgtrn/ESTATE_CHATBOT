"""Session management API endpoints."""
from typing import Any

from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import SettingsDep

router = APIRouter()


@router.post("/sessions", status_code=status.HTTP_201_CREATED)
async def create_session(settings: SettingsDep) -> dict[str, Any]:
    """Create a new conversation session."""
    return {
        "session_id": "session_123",
        "status": "active",
        "created_at": "2025-01-01T00:00:00Z",
    }


@router.get("/sessions/{session_id}")
async def get_session(session_id: str, settings: SettingsDep) -> dict[str, Any]:
    """Get session details."""
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )
    return {
        "session_id": session_id,
        "status": "active",
        "created_at": "2025-01-01T00:00:00Z",
    }


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(session_id: str, settings: SettingsDep) -> None:
    """Delete a session."""
    pass
