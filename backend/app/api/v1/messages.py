"""Message handling API endpoints."""
from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.api.dependencies import SettingsDep

router = APIRouter()


class MessageRequest(BaseModel):
    """Message request model."""

    message: str
    language: str = "ja"


@router.post("/sessions/{session_id}/messages")
async def send_message(
    session_id: str,
    request: MessageRequest,
    settings: SettingsDep,
) -> dict[str, Any]:
    """Send a message in a conversation."""
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )

    return {
        "message_id": "msg_123",
        "session_id": session_id,
        "response": "こんにちは！お探しの物件について教えてください。",
        "intent": "greeting",
        "entities": [],
    }


@router.get("/sessions/{session_id}/messages")
async def get_messages(session_id: str, settings: SettingsDep) -> dict[str, Any]:
    """Get all messages in a session."""
    return {
        "session_id": session_id,
        "messages": [],
        "total": 0,
    }
