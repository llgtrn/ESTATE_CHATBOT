"""Test data and fixtures for testing."""
from datetime import datetime, timedelta
from typing import Any

from app.db.models import BriefStatus, PropertyType, SessionStatus

# Sample session data
SAMPLE_SESSIONS = [
    {
        "id": "session_001",
        "user_id": "user_001",
        "status": SessionStatus.ACTIVE,
        "language": "ja",
        "turn_count": 5,
        "token_count": 1500,
        "metadata": {"source": "web", "device": "desktop"},
    },
    {
        "id": "session_002",
        "user_id": "user_002",
        "status": SessionStatus.ACTIVE,
        "language": "en",
        "turn_count": 3,
        "token_count": 800,
        "metadata": {"source": "mobile", "device": "ios"},
    },
    {
        "id": "session_003",
        "user_id": None,
        "status": SessionStatus.COMPLETED,
        "language": "ja",
        "turn_count": 10,
        "token_count": 3000,
        "metadata": {},
    },
    {
        "id": "session_004",
        "status": SessionStatus.EXPIRED,
        "language": "vi",
        "turn_count": 2,
        "token_count": 400,
        "metadata": {"source": "web"},
    },
]

# Sample message data
SAMPLE_MESSAGES = [
    {
        "id": "msg_001",
        "session_id": "session_001",
        "role": "user",
        "content": "マンションを買いたいです",
        "language": "ja",
        "intent": "property_search_buy",
        "confidence": 0.95,
        "entities": {"property_type": "マンション"},
        "metadata": {},
        "token_count": 50,
    },
    {
        "id": "msg_002",
        "session_id": "session_001",
        "role": "assistant",
        "content": "マンション購入のお手伝いをいたします。ご予算はどのくらいでしょうか？",
        "language": "ja",
        "intent": None,
        "confidence": None,
        "entities": {},
        "metadata": {},
        "token_count": 150,
    },
    {
        "id": "msg_003",
        "session_id": "session_001",
        "role": "user",
        "content": "予算は5000万円です",
        "language": "ja",
        "intent": "provide_budget",
        "confidence": 0.92,
        "entities": {"budget": 50000000},
        "metadata": {},
        "token_count": 45,
    },
    {
        "id": "msg_004",
        "session_id": "session_002",
        "role": "user",
        "content": "I want to rent an apartment",
        "language": "en",
        "intent": "property_search_rent",
        "confidence": 0.88,
        "entities": {"property_type": "apartment"},
        "metadata": {},
        "token_count": 60,
    },
]

# Sample brief data
SAMPLE_BRIEFS = [
    {
        "id": "brief_001",
        "session_id": "session_001",
        "property_type": PropertyType.BUY,
        "status": BriefStatus.IN_PROGRESS,
        "location": "東京都渋谷区",
        "budget_min": 50000000,
        "budget_max": 80000000,
        "rooms": "3LDK",
        "area_min": 70.0,
        "area_max": 90.0,
        "data": {
            "preferred_floor": "5階以上",
            "parking": True,
            "pet_friendly": False,
        },
        "extracted_entities": {
            "budget": 50000000,
            "rooms": "3LDK",
            "location": "渋谷区",
        },
        "completeness_score": 85.0,
        "lead_score": 78.5,
    },
    {
        "id": "brief_002",
        "session_id": "session_002",
        "property_type": PropertyType.RENT,
        "status": BriefStatus.DRAFT,
        "location": "Shibuya, Tokyo",
        "budget_min": 150000,
        "budget_max": 200000,
        "rooms": "2LDK",
        "data": {},
        "extracted_entities": {},
        "completeness_score": 50.0,
        "lead_score": 45.0,
    },
    {
        "id": "brief_003",
        "session_id": "session_003",
        "property_type": PropertyType.SELL,
        "status": BriefStatus.SUBMITTED,
        "location": "横浜市",
        "asking_price": 75000000,
        "rooms": "4LDK",
        "property_age": 15,
        "data": {
            "building_type": "一戸建て",
            "land_area": 120.0,
            "building_area": 150.0,
        },
        "extracted_entities": {
            "location": "横浜市",
            "asking_price": 75000000,
        },
        "completeness_score": 95.0,
        "lead_score": 88.0,
        "submitted_at": datetime.utcnow(),
    },
]

# Sample glossary terms
SAMPLE_GLOSSARY_TERMS = [
    {
        "id": "term_001",
        "term": "築年数",
        "language": "ja",
        "translation": "Building Age",
        "explanation": "建物が建築されてから経過した年数。古い建物ほど価値が下がる傾向がある。",
        "category": "property_info",
        "synonyms": ["建築年数", "経過年数"],
        "examples": ["築10年のマンション", "築浅物件"],
        "usage_count": 150,
        "metadata": {"verified": True},
    },
    {
        "id": "term_002",
        "term": "敷金",
        "language": "ja",
        "translation": "Security Deposit",
        "explanation": "賃貸契約時に貸主に預けるお金。退去時に原状回復費用を差し引いて返金される。",
        "category": "rental",
        "synonyms": ["保証金"],
        "examples": ["敷金2ヶ月", "敷金礼金なし"],
        "usage_count": 200,
        "metadata": {},
    },
    {
        "id": "term_003",
        "term": "2LDK",
        "language": "ja",
        "translation": "2 Bedrooms + Living/Dining/Kitchen",
        "explanation": "リビング・ダイニング・キッチンと2つの部屋がある間取り。",
        "category": "layout",
        "synonyms": [],
        "examples": ["2LDK 70㎡", "広々2LDK"],
        "usage_count": 300,
        "metadata": {},
    },
    {
        "id": "term_004",
        "term": "Security Deposit",
        "language": "en",
        "translation": "敷金",
        "explanation": "Money paid to the landlord at the start of a tenancy, refunded after deducting repair costs.",
        "category": "rental",
        "synonyms": ["Deposit"],
        "examples": ["2 months security deposit", "No deposit required"],
        "usage_count": 50,
        "metadata": {},
    },
    {
        "id": "term_005",
        "term": "Tiền đặt cọc",
        "language": "vi",
        "translation": "Security Deposit / 敷金",
        "explanation": "Số tiền trả cho chủ nhà khi bắt đầu thuê, sẽ được hoàn lại sau khi trừ chi phí sửa chữa.",
        "category": "rental",
        "synonyms": ["Tiền cọc"],
        "examples": ["Đặt cọc 2 tháng", "Không cần đặt cọc"],
        "usage_count": 25,
        "metadata": {},
    },
]

# Sample NLU test cases
NLU_TEST_CASES = [
    {
        "input": "マンションを買いたいです",
        "expected_intent": "property_search_buy",
        "expected_entities": {},
        "language": "ja",
    },
    {
        "input": "予算は5000万円で3LDKを探しています",
        "expected_intent": "property_search_buy",
        "expected_entities": {"budget": 50000000, "rooms": "3LDK"},
        "language": "ja",
    },
    {
        "input": "渋谷区で賃貸を探しています",
        "expected_intent": "property_search_rent",
        "expected_entities": {"location": "渋谷区"},
        "language": "ja",
    },
    {
        "input": "I want to buy an apartment in Tokyo",
        "expected_intent": "property_search_buy",
        "expected_entities": {"location": "Tokyo"},
        "language": "en",
    },
    {
        "input": "築年数とは何ですか",
        "expected_intent": "glossary_query",
        "expected_entities": {"term": "築年数"},
        "language": "ja",
    },
    {
        "input": "ありがとうございます",
        "expected_intent": "thanking",
        "expected_entities": {},
        "language": "ja",
    },
]

# Sample conversation flows
CONVERSATION_FLOWS = {
    "buy_flow_ja": [
        {"role": "user", "content": "マンションを買いたいです", "intent": "property_search_buy"},
        {"role": "assistant", "content": "マンション購入のお手伝いをいたします。"},
        {"role": "user", "content": "予算は5000万円です", "intent": "provide_budget"},
        {"role": "assistant", "content": "ご予算5000万円ですね。"},
        {"role": "user", "content": "渋谷区で探しています", "intent": "provide_location"},
        {"role": "assistant", "content": "渋谷区での物件をお探しですね。"},
        {"role": "user", "content": "3LDKが希望です", "intent": "provide_rooms"},
        {"role": "assistant", "content": "3LDKの物件ですね。"},
    ],
    "rent_flow_en": [
        {"role": "user", "content": "I want to rent an apartment", "intent": "property_search_rent"},
        {"role": "assistant", "content": "I can help you find a rental property."},
        {"role": "user", "content": "My budget is 150,000 yen per month", "intent": "provide_budget"},
        {"role": "assistant", "content": "Budget of 150,000 yen per month."},
        {"role": "user", "content": "In Shibuya area", "intent": "provide_location"},
        {"role": "assistant", "content": "Looking in Shibuya area."},
    ],
    "sell_flow_ja": [
        {"role": "user", "content": "マンションを売りたいです", "intent": "property_sell"},
        {"role": "assistant", "content": "売却のお手伝いをいたします。"},
        {"role": "user", "content": "港区にあります", "intent": "provide_location"},
        {"role": "assistant", "content": "港区の物件ですね。"},
        {"role": "user", "content": "8000万円で売りたいです", "intent": "provide_price"},
        {"role": "assistant", "content": "希望売却価格8000万円ですね。"},
    ],
}

# Sample PII data for safety testing
PII_TEST_CASES = [
    {
        "input": "メールアドレスはtest@example.comです",
        "expected_masked": "メールアドレスは[EMAIL]です",
        "detected_pii": ["email"],
    },
    {
        "input": "電話番号は03-1234-5678です",
        "expected_masked": "電話番号は[PHONE]です",
        "detected_pii": ["phone"],
    },
    {
        "input": "My email is user@test.com and phone is 090-1234-5678",
        "expected_masked": "My email is [EMAIL] and phone is [PHONE]",
        "detected_pii": ["email", "phone"],
    },
]

# Sample content filtering test cases
CONTENT_FILTER_TEST_CASES = [
    {
        "input": "マンションを買いたいです",
        "is_safe": True,
        "is_spam": False,
    },
    {
        "input": "Buy now! Limited offer! Click here!!!",
        "is_safe": True,
        "is_spam": True,
    },
    {
        "input": "こんにちは",
        "is_safe": True,
        "is_spam": False,
    },
]

# Sample affordability test cases
AFFORDABILITY_TEST_CASES = [
    {
        "annual_income": 10000000,  # 10M yen
        "down_payment": 20000000,  # 20M yen
        "interest_rate": 0.01,  # 1%
        "loan_years": 35,
        "expected_max_loan": 70000000,  # 7x income
        "expected_max_price": 90000000,  # loan + down payment
    },
    {
        "annual_income": 8000000,
        "down_payment": 15000000,
        "interest_rate": 0.015,
        "loan_years": 30,
        "expected_max_loan": 56000000,
        "expected_max_price": 71000000,
    },
    {
        "annual_income": 12000000,
        "down_payment": 30000000,
        "interest_rate": 0.008,
        "loan_years": 35,
        "expected_max_loan": 84000000,
        "expected_max_price": 114000000,
    },
]

# Sample lead scoring test cases
LEAD_SCORING_TEST_CASES = [
    {
        "completeness_score": 100.0,
        "has_budget": True,
        "has_location": True,
        "has_rooms": True,
        "has_timeline": True,
        "expected_score_range": (85.0, 100.0),
    },
    {
        "completeness_score": 50.0,
        "has_budget": True,
        "has_location": False,
        "has_rooms": False,
        "has_timeline": False,
        "expected_score_range": (40.0, 60.0),
    },
    {
        "completeness_score": 25.0,
        "has_budget": False,
        "has_location": False,
        "has_rooms": False,
        "has_timeline": False,
        "expected_score_range": (0.0, 30.0),
    },
]


def create_sample_session(
    session_id: str = "test_session",
    status: SessionStatus = SessionStatus.ACTIVE,
    language: str = "ja",
    **kwargs: Any,
) -> dict[str, Any]:
    """Create a sample session dictionary."""
    return {
        "id": session_id,
        "user_id": kwargs.get("user_id"),
        "status": status,
        "language": language,
        "turn_count": kwargs.get("turn_count", 0),
        "token_count": kwargs.get("token_count", 0),
        "metadata": kwargs.get("metadata", {}),
        "created_at": kwargs.get("created_at", datetime.utcnow()),
        "updated_at": kwargs.get("updated_at", datetime.utcnow()),
        "expires_at": kwargs.get("expires_at"),
    }


def create_sample_message(
    message_id: str = "test_msg",
    session_id: str = "test_session",
    role: str = "user",
    content: str = "Test message",
    **kwargs: Any,
) -> dict[str, Any]:
    """Create a sample message dictionary."""
    return {
        "id": message_id,
        "session_id": session_id,
        "role": role,
        "content": content,
        "language": kwargs.get("language", "ja"),
        "intent": kwargs.get("intent"),
        "confidence": kwargs.get("confidence"),
        "entities": kwargs.get("entities", {}),
        "metadata": kwargs.get("metadata", {}),
        "token_count": kwargs.get("token_count", 0),
        "created_at": kwargs.get("created_at", datetime.utcnow()),
    }


def create_sample_brief(
    brief_id: str = "test_brief",
    session_id: str = "test_session",
    property_type: PropertyType = PropertyType.BUY,
    **kwargs: Any,
) -> dict[str, Any]:
    """Create a sample brief dictionary."""
    return {
        "id": brief_id,
        "session_id": session_id,
        "property_type": property_type,
        "status": kwargs.get("status", BriefStatus.DRAFT),
        "location": kwargs.get("location"),
        "budget_min": kwargs.get("budget_min"),
        "budget_max": kwargs.get("budget_max"),
        "rooms": kwargs.get("rooms"),
        "area_min": kwargs.get("area_min"),
        "area_max": kwargs.get("area_max"),
        "data": kwargs.get("data", {}),
        "extracted_entities": kwargs.get("extracted_entities", {}),
        "completeness_score": kwargs.get("completeness_score", 0.0),
        "lead_score": kwargs.get("lead_score", 0.0),
        "created_at": kwargs.get("created_at", datetime.utcnow()),
        "updated_at": kwargs.get("updated_at", datetime.utcnow()),
        "submitted_at": kwargs.get("submitted_at"),
    }


def create_sample_glossary_term(
    term_id: str = "test_term",
    term: str = "Test Term",
    language: str = "ja",
    **kwargs: Any,
) -> dict[str, Any]:
    """Create a sample glossary term dictionary."""
    return {
        "id": term_id,
        "term": term,
        "language": language,
        "translation": kwargs.get("translation", "Test Translation"),
        "explanation": kwargs.get("explanation", "Test explanation"),
        "category": kwargs.get("category"),
        "synonyms": kwargs.get("synonyms", []),
        "examples": kwargs.get("examples", []),
        "usage_count": kwargs.get("usage_count", 0),
        "metadata": kwargs.get("metadata", {}),
        "created_at": kwargs.get("created_at", datetime.utcnow()),
        "updated_at": kwargs.get("updated_at", datetime.utcnow()),
    }
