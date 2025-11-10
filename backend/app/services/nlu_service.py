"""NLU service for natural language understanding."""
import logging
import re
from typing import Any

from app.utils.language import detect_language

logger = logging.getLogger(__name__)


class NLUService:
    """Service for natural language understanding."""

    def __init__(self) -> None:
        """Initialize NLU service."""
        self.intent_patterns = self._load_intent_patterns()
        self.entity_patterns = self._load_entity_patterns()

    def _load_intent_patterns(self) -> dict[str, list[str]]:
        """Load intent patterns."""
        return {
            "greeting": [
                r"こんにちは",
                r"はじめまして",
                r"hello",
                r"hi",
                r"xin chào",
            ],
            "property_search_buy": [
                r"買いたい",
                r"購入",
                r"buy",
                r"purchase",
                r"mua",
            ],
            "property_search_rent": [
                r"借りたい",
                r"賃貸",
                r"rent",
                r"thuê",
            ],
            "property_search_sell": [
                r"売りたい",
                r"売却",
                r"sell",
                r"bán",
            ],
            "location_query": [
                r"どこ",
                r"場所",
                r"where",
                r"location",
                r"ở đâu",
            ],
            "budget_query": [
                r"予算",
                r"いくら",
                r"budget",
                r"price",
                r"ngân sách",
            ],
            "confirmation": [
                r"はい",
                r"そうです",
                r"yes",
                r"correct",
                r"đúng",
            ],
            "negation": [
                r"いいえ",
                r"違います",
                r"no",
                r"wrong",
                r"không",
            ],
        }

    def _load_entity_patterns(self) -> dict[str, str]:
        """Load entity extraction patterns."""
        return {
            "budget": r"(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:万円|円|yen|万|million)?",
            "rooms": r"(\d+[LSDK]+|studio|ワンルーム)",
            "area": r"(\d+(?:\.\d+)?)\s*(?:㎡|平米|m2|m²|坪)",
            "location_ja": r"(東京|大阪|名古屋|福岡|横浜|神奈川|千葉|埼玉|[都道府県市区町村])",
        }

    async def analyze(
        self,
        text: str,
        language: str | None = None,
    ) -> dict[str, Any]:
        """Analyze text for intent and entities."""
        if not language:
            language = detect_language(text)

        logger.info(f"Analyzing text in {language}: {text[:50]}...")

        # Detect intent
        intent, confidence = self._detect_intent(text)

        # Extract entities
        entities = self._extract_entities(text)

        return {
            "intent": intent,
            "confidence": confidence,
            "entities": entities,
            "language": language,
        }

    def _detect_intent(self, text: str) -> tuple[str | None, float]:
        """Detect intent from text."""
        text_lower = text.lower()
        matched_intents: list[tuple[str, float]] = []

        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    # Simple confidence based on pattern match
                    confidence = 0.8
                    matched_intents.append((intent, confidence))
                    break

        if not matched_intents:
            return None, 0.0

        # Return intent with highest confidence
        matched_intents.sort(key=lambda x: x[1], reverse=True)
        return matched_intents[0]

    def _extract_entities(self, text: str) -> dict[str, Any]:
        """Extract entities from text."""
        entities: dict[str, Any] = {}

        # Extract budget
        budget_match = re.search(self.entity_patterns["budget"], text)
        if budget_match:
            budget_str = budget_match.group(1).replace(",", "")
            try:
                budget_value = float(budget_str)
                # Convert 万円 to yen
                if "万" in text:
                    budget_value *= 10000
                entities["budget"] = int(budget_value)
            except ValueError:
                pass

        # Extract rooms
        rooms_match = re.search(self.entity_patterns["rooms"], text, re.IGNORECASE)
        if rooms_match:
            entities["rooms"] = rooms_match.group(1).upper()

        # Extract area
        area_match = re.search(self.entity_patterns["area"], text)
        if area_match:
            try:
                area_value = float(area_match.group(1))
                entities["area"] = area_value
            except ValueError:
                pass

        # Extract location
        location_match = re.search(self.entity_patterns["location_ja"], text)
        if location_match:
            entities["location"] = location_match.group(1)

        return entities

    def validate_entities(self, entities: dict[str, Any]) -> list[str]:
        """Validate extracted entities."""
        errors = []

        # Validate budget
        if "budget" in entities:
            budget = entities["budget"]
            if budget <= 0:
                errors.append("Budget must be positive")
            if budget > 10_000_000_000:  # 100億円
                errors.append("Budget is too high")

        # Validate area
        if "area" in entities:
            area = entities["area"]
            if area <= 0:
                errors.append("Area must be positive")
            if area > 10000:  # 10000㎡
                errors.append("Area is too large")

        return errors
