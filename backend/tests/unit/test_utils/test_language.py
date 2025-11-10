"""Tests for language utilities."""
from app.utils.language import detect_language, is_valid_text, normalize_text


class TestDetectLanguage:
    """Tests for detect_language function."""

    def test_detect_japanese(self) -> None:
        """Test Japanese detection."""
        text = "東京で物件を探しています"
        assert detect_language(text) == "ja"

    def test_detect_japanese_hiragana(self) -> None:
        """Test Japanese hiragana detection."""
        text = "こんにちは"
        assert detect_language(text) == "ja"

    def test_detect_japanese_katakana(self) -> None:
        """Test Japanese katakana detection."""
        text = "マンション"
        assert detect_language(text) == "ja"

    def test_detect_japanese_kanji(self) -> None:
        """Test Japanese kanji detection."""
        text = "不動産"
        assert detect_language(text) == "ja"

    def test_detect_vietnamese(self) -> None:
        """Test Vietnamese detection."""
        text = "Tôi đang tìm kiếm nhà"
        assert detect_language(text) == "vi"

    def test_detect_english(self) -> None:
        """Test English detection."""
        text = "I am looking for a house"
        assert detect_language(text) == "en"

    def test_detect_empty_text(self) -> None:
        """Test empty text defaults to Japanese."""
        assert detect_language("") == "ja"

    def test_detect_mixed_ja_en(self) -> None:
        """Test mixed Japanese and English."""
        text = "Tokyo 2LDK マンション"
        assert detect_language(text) == "ja"


class TestNormalizeText:
    """Tests for normalize_text function."""

    def test_strip_whitespace(self) -> None:
        """Test whitespace stripping."""
        text = "  hello world  "
        assert normalize_text(text) == "hello world"

    def test_remove_multiple_spaces(self) -> None:
        """Test multiple space removal."""
        text = "hello    world"
        assert normalize_text(text) == "hello world"

    def test_normalize_newlines(self) -> None:
        """Test newline normalization."""
        text = "hello\n\nworld"
        assert normalize_text(text) == "hello world"

    def test_normalize_tabs(self) -> None:
        """Test tab normalization."""
        text = "hello\t\tworld"
        assert normalize_text(text) == "hello world"

    def test_normalize_empty_text(self) -> None:
        """Test empty text."""
        assert normalize_text("") == ""

    def test_normalize_japanese_text(self) -> None:
        """Test Japanese text normalization."""
        text = "  東京  で  物件  "
        assert normalize_text(text) == "東京 で 物件"


class TestIsValidText:
    """Tests for is_valid_text function."""

    def test_valid_text(self) -> None:
        """Test valid text."""
        assert is_valid_text("hello")

    def test_empty_text(self) -> None:
        """Test empty text is invalid."""
        assert not is_valid_text("")

    def test_whitespace_only(self) -> None:
        """Test whitespace-only text is invalid."""
        assert not is_valid_text("   ")

    def test_min_length(self) -> None:
        """Test minimum length validation."""
        assert is_valid_text("ab", min_length=2)
        assert not is_valid_text("a", min_length=2)

    def test_max_length(self) -> None:
        """Test maximum length validation."""
        assert is_valid_text("hello", max_length=10)
        assert not is_valid_text("hello world", max_length=5)

    def test_custom_length_range(self) -> None:
        """Test custom length range."""
        text = "hello"
        assert is_valid_text(text, min_length=3, max_length=10)
        assert not is_valid_text(text, min_length=10, max_length=20)

    def test_japanese_text(self) -> None:
        """Test Japanese text validation."""
        text = "東京"
        assert is_valid_text(text, min_length=1, max_length=100)
