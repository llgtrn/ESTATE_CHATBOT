"""Language detection and utilities."""
import logging
import re

logger = logging.getLogger(__name__)


def detect_language(text: str) -> str:
    """Detect language of text.

    Args:
        text: Input text

    Returns:
        Language code (ja, en, vi)
    """
    if not text:
        return "ja"  # Default to Japanese

    # Simple heuristic: check for Japanese characters
    if re.search(r"[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]", text):
        return "ja"

    # Check for Vietnamese characters
    if re.search(r"[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]", text):
        return "vi"

    return "en"


def normalize_text(text: str) -> str:
    """Normalize text for processing.

    Args:
        text: Input text

    Returns:
        Normalized text
    """
    if not text:
        return ""

    # Strip whitespace
    text = text.strip()

    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text


def is_valid_text(text: str, min_length: int = 1, max_length: int = 1000) -> bool:
    """Validate text length.

    Args:
        text: Input text
        min_length: Minimum length
        max_length: Maximum length

    Returns:
        True if valid
    """
    if not text:
        return False

    text_length = len(text.strip())
    return min_length <= text_length <= max_length
