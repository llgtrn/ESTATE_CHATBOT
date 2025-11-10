"""Tests for safety service."""
import pytest

from app.core.exceptions import ContentFilterError
from app.services.safety_service import SafetyService


class TestSafetyService:
    """Tests for SafetyService class."""

    def test_init(self) -> None:
        """Test service initialization."""
        service = SafetyService()
        assert service is not None
        assert service.blocked_patterns is not None
        assert service.pii_patterns is not None

    @pytest.mark.asyncio
    async def test_filter_content_safe(self) -> None:
        """Test filtering safe content."""
        service = SafetyService()
        result = await service.filter_content("東京で物件を探しています")

        assert result["is_safe"]
        assert result["reason"] is None
        assert result["filtered_text"] is not None

    @pytest.mark.asyncio
    async def test_filter_content_spam(self) -> None:
        """Test filtering spam content."""
        service = SafetyService()
        result = await service.filter_content("This is spam and scam")

        assert not result["is_safe"]
        assert result["reason"] == "inappropriate_content"
        assert result["filtered_text"] is None

    @pytest.mark.asyncio
    async def test_filter_content_too_long(self) -> None:
        """Test filtering content that's too long."""
        service = SafetyService()
        long_text = "a" * 15000
        result = await service.filter_content(long_text)

        assert not result["is_safe"]
        assert result["reason"] == "text_too_long"

    @pytest.mark.asyncio
    async def test_mask_pii_email(self) -> None:
        """Test masking email addresses."""
        service = SafetyService()
        text = "My email is user@example.com"
        result = await service.mask_pii(text)

        assert result["has_pii"]
        assert "email" in result["detected_pii"]
        assert "[EMAIL]" in result["masked_text"]
        assert "user@example.com" not in result["masked_text"]

    @pytest.mark.asyncio
    async def test_mask_pii_phone_japanese(self) -> None:
        """Test masking Japanese phone numbers."""
        service = SafetyService()
        text = "電話番号は 03-1234-5678 です"
        result = await service.mask_pii(text)

        assert result["has_pii"]
        assert "phone" in result["detected_pii"]
        assert "[PHONE]" in result["masked_text"]
        assert "03-1234-5678" not in result["masked_text"]

    @pytest.mark.asyncio
    async def test_mask_pii_credit_card(self) -> None:
        """Test masking credit card numbers."""
        service = SafetyService()
        text = "Card: 1234 5678 9012 3456"
        result = await service.mask_pii(text)

        assert result["has_pii"]
        assert "credit_card" in result["detected_pii"]
        assert "[CREDIT_CARD]" in result["masked_text"]

    @pytest.mark.asyncio
    async def test_mask_pii_no_pii(self) -> None:
        """Test text with no PII."""
        service = SafetyService()
        text = "東京で物件を探しています"
        result = await service.mask_pii(text)

        assert not result["has_pii"]
        assert result["detected_pii"] == []
        assert result["masked_text"] == text

    @pytest.mark.asyncio
    async def test_mask_pii_multiple(self) -> None:
        """Test masking multiple PII types."""
        service = SafetyService()
        text = "Contact me at user@example.com or 03-1234-5678"
        result = await service.mask_pii(text)

        assert result["has_pii"]
        assert "email" in result["detected_pii"]
        assert "phone" in result["detected_pii"]
        assert "[EMAIL]" in result["masked_text"]
        assert "[PHONE]" in result["masked_text"]

    @pytest.mark.asyncio
    async def test_validate_message_safe(self) -> None:
        """Test validating safe message."""
        service = SafetyService()
        result = await service.validate_message("東京で物件を探しています")

        assert result["is_safe"]
        assert result["filtered_text"] is not None

    @pytest.mark.asyncio
    async def test_validate_message_unsafe(self) -> None:
        """Test validating unsafe message."""
        service = SafetyService()

        with pytest.raises(ContentFilterError):
            await service.validate_message("This is spam and scam")

    @pytest.mark.asyncio
    async def test_validate_message_with_pii(self) -> None:
        """Test validating message with PII."""
        service = SafetyService()
        result = await service.validate_message("Contact: user@example.com")

        assert result["is_safe"]
        assert result["has_pii"]
        assert "[EMAIL]" in result["filtered_text"]

    @pytest.mark.asyncio
    async def test_detect_spam_repeated_chars(self) -> None:
        """Test detecting spam with repeated characters."""
        service = SafetyService()
        is_spam = await service.detect_spam("aaaaaaaaaa", 0)

        assert is_spam

    @pytest.mark.asyncio
    async def test_detect_spam_excessive_caps(self) -> None:
        """Test detecting spam with excessive capitalization."""
        service = SafetyService()
        is_spam = await service.detect_spam("THIS IS ALL CAPITALS!!!!!", 0)

        assert is_spam

    @pytest.mark.asyncio
    async def test_detect_spam_flooding(self) -> None:
        """Test detecting message flooding."""
        service = SafetyService()
        is_spam = await service.detect_spam("normal message", 150)

        assert is_spam

    @pytest.mark.asyncio
    async def test_detect_spam_normal_message(self) -> None:
        """Test detecting normal message as not spam."""
        service = SafetyService()
        is_spam = await service.detect_spam("東京で物件を探しています", 5)

        assert not is_spam

    @pytest.mark.asyncio
    async def test_check_abuse_clean(self) -> None:
        """Test checking abuse for clean message."""
        service = SafetyService()
        result = await service.check_abuse("東京で物件を探しています")

        assert not result["is_abuse"]
        assert result["reasons"] == []
        assert result["action"] == "allow"

    @pytest.mark.asyncio
    async def test_check_abuse_with_spam(self) -> None:
        """Test checking abuse with spam."""
        service = SafetyService()
        result = await service.check_abuse("aaaaaaaaaa")

        assert result["is_abuse"]
        assert "spam_detected" in result["reasons"]
        assert result["action"] == "block"

    @pytest.mark.asyncio
    async def test_check_abuse_with_inappropriate_content(self) -> None:
        """Test checking abuse with inappropriate content."""
        service = SafetyService()
        result = await service.check_abuse("This is spam and scam")

        assert result["is_abuse"]
        assert "content_policy_violation" in result["reasons"]
        assert result["action"] == "block"
