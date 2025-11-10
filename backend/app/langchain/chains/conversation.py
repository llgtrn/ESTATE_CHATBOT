"""Main conversation chain for the chatbot."""
import logging
from typing import Any

logger = logging.getLogger(__name__)


class ConversationChain:
    """Main conversation chain handler."""

    def __init__(self, model_name: str = "gemini-1.5-flash-002") -> None:
        """Initialize conversation chain."""
        self.model_name = model_name
        logger.info(f"Initialized ConversationChain with model: {model_name}")
        self._initialize_prompts()

    def _initialize_prompts(self) -> None:
        """Initialize prompt templates."""
        self.system_prompt = """あなたは不動産物件を探している顧客をサポートする親切なアシスタントです。
顧客のニーズを理解し、物件探しに必要な情報を収集してください。

必要な情報:
- 物件タイプ (購入/賃貸/売却)
- 場所/エリア
- 予算
- 間取り (1K, 2LDK など)
- その他の希望条件

自然な会話で情報を引き出し、顧客に寄り添った対応を心がけてください。"""

    async def process_message(self, message: str, context: dict[str, Any]) -> dict[str, Any]:
        """Process a user message and return response."""
        logger.info(f"Processing message: {message[:50]}...")

        # Get intent and entities from context
        intent = context.get("intent")
        entities = context.get("entities", {})
        language = context.get("language", "ja")

        # Generate response based on intent
        response = self._generate_response(message, intent, entities, language)

        return {
            "response": response,
            "intent": intent,
            "confidence": 0.85,
            "model": self.model_name,
        }

    def _generate_response(
        self,
        message: str,
        intent: str | None,
        entities: dict[str, Any],
        language: str,
    ) -> str:
        """Generate response based on intent and entities."""
        # Intent-based responses (Japanese)
        if language == "ja":
            if intent == "greeting":
                return "こんにちは！不動産物件のご相談ですね。どのような物件をお探しですか？（購入・賃貸・売却）"

            if intent == "property_search_buy":
                if "location" in entities:
                    location = entities["location"]
                    return f"{location}での購入をご検討されているのですね。ご予算はどのくらいでしょうか？"
                return "購入をご希望なのですね。どのエリアをお探しですか？"

            if intent == "property_search_rent":
                if "budget" in entities:
                    budget = entities["budget"]
                    return f"ご予算{budget:,}円ですね。どのエリアをお探しですか？"
                return "賃貸をご希望なのですね。ご希望のエリアとご予算を教えていただけますか？"

            if intent == "property_search_sell":
                return "売却のご相談ですね。物件の詳細を教えていただけますか？"

            if "budget" in entities:
                budget = entities["budget"]
                return f"ご予算{budget:,}円ですね。ご希望の間取りはありますか？（例：2LDK、3LDK）"

            if "rooms" in entities:
                rooms = entities["rooms"]
                return f"{rooms}をご希望なのですね。他にご要望はございますか？"

        # English responses
        if language == "en":
            if intent == "greeting":
                return "Hello! I'm here to help you find a property. Are you looking to buy, rent, or sell?"

            if intent == "property_search_buy":
                return "You're looking to buy. What's your budget range?"

        # Vietnamese responses
        if language == "vi":
            if intent == "greeting":
                return "Xin chào! Tôi có thể giúp bạn tìm bất động sản. Bạn muốn mua, thuê hay bán?"

        # Default response
        return "ありがとうございます。他に何かご質問はございますか？"

    def get_model_info(self) -> dict[str, str]:
        """Get model information."""
        return {"model": self.model_name, "status": "ready"}
