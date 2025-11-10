"""Safety service for content filtering and PII masking."""
import logging
import re
from typing import Any

from app.core.exceptions import ContentFilterError

logger = logging.getLogger(__name__)


class SafetyService:
    """Service for safety and content filtering."""

    def __init__(self) -> None:
        """Initialize service."""
        self.blocked_patterns = self._load_blocked_patterns()
        self.pii_patterns = self._load_pii_patterns()

    def _load_blocked_patterns(self) -> list[str]:
        """Load blocked content patterns."""
        return [
            r"(spam|scam)",
            r"(inappropriate|offensive)",
            r"(malicious|attack)",
        ]

    def _load_pii_patterns(self) -> dict[str, str]:
        """Load PII detection patterns."""
        return {
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "phone_jp": r"0\d{1,4}-?\d{1,4}-?\d{4}",
            "phone_intl": r"\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}",
            "credit_card": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        }

    async def filter_content(self, text: str) -> dict[str, Any]:
        """Filter content for inappropriate or harmful text."""
        logger.debug(f"Filtering content: {text[:50]}...")

        # Check for blocked patterns
        for pattern in self.blocked_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                logger.warning(f"Blocked pattern detected: {pattern}")
                return {
                    "is_safe": False,
                    "reason": "inappropriate_content",
                    "filtered_text": None,
                }

        # Check text length
        if len(text) > 10000:
            logger.warning("Text too long")
            return {
                "is_safe": False,
                "reason": "text_too_long",
                "filtered_text": None,
            }

        return {
            "is_safe": True,
            "reason": None,
            "filtered_text": text,
        }

    async def mask_pii(self, text: str) -> dict[str, Any]:
        """Mask personally identifiable information."""
        logger.debug(f"Masking PII in: {text[:50]}...")

        masked_text = text
        detected_pii: list[str] = []

        # Mask emails
        if re.search(self.pii_patterns["email"], masked_text):
            masked_text = re.sub(
                self.pii_patterns["email"],
                "[EMAIL]",
                masked_text,
            )
            detected_pii.append("email")

        # Mask phone numbers
        if re.search(self.pii_patterns["phone_jp"], masked_text):
            masked_text = re.sub(
                self.pii_patterns["phone_jp"],
                "[PHONE]",
                masked_text,
            )
            detected_pii.append("phone")

        if re.search(self.pii_patterns["phone_intl"], masked_text):
            masked_text = re.sub(
                self.pii_patterns["phone_intl"],
                "[PHONE]",
                masked_text,
            )
            if "phone" not in detected_pii:
                detected_pii.append("phone")

        # Mask credit cards
        if re.search(self.pii_patterns["credit_card"], masked_text):
            masked_text = re.sub(
                self.pii_patterns["credit_card"],
                "[CREDIT_CARD]",
                masked_text,
            )
            detected_pii.append("credit_card")

        return {
            "original_text": text,
            "masked_text": masked_text,
            "detected_pii": detected_pii,
            "has_pii": len(detected_pii) > 0,
        }

    async def validate_message(self, text: str) -> dict[str, Any]:
        """Validate message safety."""
        # Filter content
        filter_result = await self.filter_content(text)

        if not filter_result["is_safe"]:
            raise ContentFilterError(
                f"Content filtered: {filter_result['reason']}",
                details={"reason": filter_result["reason"]},
            )

        # Mask PII
        pii_result = await self.mask_pii(text)

        return {
            "is_safe": True,
            "filtered_text": pii_result["masked_text"],
            "detected_pii": pii_result["detected_pii"],
            "has_pii": pii_result["has_pii"],
        }

    async def detect_spam(self, text: str, session_message_count: int) -> bool:
        """Detect spam behavior."""
        # Check for repeated characters
        if re.search(r"(.)\1{5,}", text):
            logger.warning("Repeated characters detected")
            return True

        # Check for excessive capitalization
        if len(text) > 20:
            caps_ratio = sum(1 for c in text if c.isupper()) / len(text)
            if caps_ratio > 0.7:
                logger.warning("Excessive capitalization detected")
                return True

        # Check for message flooding
        if session_message_count > 100:
            logger.warning("Message flooding detected")
            return True

        return False

    async def check_abuse(
        self,
        text: str,
        user_id: str | None = None,
    ) -> dict[str, Any]:
        """Check for abusive behavior."""
        is_abuse = False
        reasons: list[str] = []

        # Check for spam patterns
        if await self.detect_spam(text, 0):
            is_abuse = True
            reasons.append("spam_detected")

        # Check for content policy violations
        filter_result = await self.filter_content(text)
        if not filter_result["is_safe"]:
            is_abuse = True
            reasons.append("content_policy_violation")

        return {
            "is_abuse": is_abuse,
            "reasons": reasons,
            "action": "block" if is_abuse else "allow",
        }
