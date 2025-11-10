"""Conversation service for handling chatbot interactions."""
import logging
from typing import Any

from app.core.exceptions import InvalidMessageError, SessionExpiredError, SessionNotFoundError
from app.db.models import SessionStatus
from app.db.repositories.message import MessageRepository
from app.db.repositories.session import SessionRepository
from app.langchain.chains.conversation import ConversationChain
from app.services.nlu_service import NLUService
from app.utils.language import detect_language, is_valid_text, normalize_text

logger = logging.getLogger(__name__)


class ConversationService:
    """Service for managing conversations."""

    def __init__(
        self,
        session_repo: SessionRepository,
        message_repo: MessageRepository,
        conversation_chain: ConversationChain,
        nlu_service: NLUService,
    ) -> None:
        """Initialize service."""
        self.session_repo = session_repo
        self.message_repo = message_repo
        self.conversation_chain = conversation_chain
        self.nlu_service = nlu_service

    async def create_session(
        self,
        language: str = "ja",
        user_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a new conversation session."""
        logger.info(f"Creating new session with language: {language}")

        session = await self.session_repo.create(
            language=language,
            user_id=user_id,
            metadata=metadata or {},
        )

        return {
            "session_id": session.id,
            "status": session.status.value,
            "language": session.language,
            "created_at": session.created_at.isoformat(),
            "expires_at": session.expires_at.isoformat() if session.expires_at else None,
        }

    async def get_session(self, session_id: str) -> dict[str, Any]:
        """Get session details."""
        session = await self.session_repo.get_by_id(session_id)

        if not session:
            raise SessionNotFoundError(session_id)

        if session.status == SessionStatus.EXPIRED:
            raise SessionExpiredError(session_id)

        return {
            "session_id": session.id,
            "status": session.status.value,
            "language": session.language,
            "turn_count": session.turn_count,
            "token_count": session.token_count,
            "created_at": session.created_at.isoformat(),
            "updated_at": session.updated_at.isoformat(),
        }

    async def send_message(
        self,
        session_id: str,
        message: str,
        language: str | None = None,
    ) -> dict[str, Any]:
        """Process user message and generate response."""
        # Validate session
        session = await self.session_repo.get_by_id(session_id)
        if not session:
            raise SessionNotFoundError(session_id)

        if session.status != SessionStatus.ACTIVE:
            raise SessionExpiredError(session_id)

        # Validate message
        normalized_message = normalize_text(message)
        if not is_valid_text(normalized_message):
            raise InvalidMessageError("Message is empty or invalid")

        # Detect language if not provided
        detected_language = language or detect_language(normalized_message)

        logger.info(
            f"Processing message for session {session_id}: {normalized_message[:50]}..."
        )

        # Perform NLU analysis
        nlu_result = await self.nlu_service.analyze(
            text=normalized_message,
            language=detected_language,
        )

        # Save user message
        user_message = await self.message_repo.create(
            session_id=session_id,
            role="user",
            content=normalized_message,
            language=detected_language,
            intent=nlu_result.get("intent"),
            confidence=nlu_result.get("confidence"),
            entities=nlu_result.get("entities", {}),
        )

        # Get conversation history
        history = await self.message_repo.get_recent_messages(session_id, count=10)

        # Generate response
        context = {
            "session_id": session_id,
            "language": detected_language,
            "history": [
                {"role": msg.role, "content": msg.content} for msg in history
            ],
            "intent": nlu_result.get("intent"),
            "entities": nlu_result.get("entities", {}),
        }

        response_data = await self.conversation_chain.process_message(
            normalized_message, context
        )

        # Save assistant response
        assistant_message = await self.message_repo.create(
            session_id=session_id,
            role="assistant",
            content=response_data["response"],
            language=detected_language,
        )

        # Update session stats
        await self.session_repo.increment_turn_count(session_id)

        return {
            "message_id": assistant_message.id,
            "session_id": session_id,
            "response": response_data["response"],
            "intent": nlu_result.get("intent"),
            "confidence": nlu_result.get("confidence"),
            "entities": nlu_result.get("entities", {}),
            "language": detected_language,
        }

    async def get_messages(
        self,
        session_id: str,
        limit: int | None = None,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Get conversation history."""
        session = await self.session_repo.get_by_id(session_id)
        if not session:
            raise SessionNotFoundError(session_id)

        messages = await self.message_repo.get_by_session(
            session_id=session_id,
            limit=limit,
            offset=offset,
        )

        total_count = await self.message_repo.count_by_session(session_id)

        return {
            "session_id": session_id,
            "messages": [
                {
                    "message_id": msg.id,
                    "role": msg.role,
                    "content": msg.content,
                    "language": msg.language,
                    "intent": msg.intent,
                    "confidence": msg.confidence,
                    "entities": msg.entities,
                    "created_at": msg.created_at.isoformat(),
                }
                for msg in messages
            ],
            "total": total_count,
            "limit": limit,
            "offset": offset,
        }

    async def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        logger.info(f"Deleting session: {session_id}")
        return await self.session_repo.delete(session_id)

    async def cleanup_expired_sessions(self) -> int:
        """Cleanup expired sessions."""
        logger.info("Cleaning up expired sessions")
        return await self.session_repo.cleanup_expired_sessions()
