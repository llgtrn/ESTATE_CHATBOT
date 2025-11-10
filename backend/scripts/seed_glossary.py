#!/usr/bin/env python3
"""Seed glossary data into the database."""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import get_settings
from app.db.repositories.glossary import GlossaryRepository

# Sample glossary terms
GLOSSARY_TERMS = [
    {
        "term": "築年数",
        "language": "ja",
        "translation": "Building Age",
        "explanation": "建物が建築されてから経過した年数。古い建物ほど価値が下がる傾向がある。",
        "category": "property_info",
        "synonyms": ["建築年数", "経過年数"],
        "examples": ["築10年のマンション", "築浅物件"],
    },
    {
        "term": "敷金",
        "language": "ja",
        "translation": "Security Deposit",
        "explanation": "賃貸契約時に貸主に預けるお金。退去時に原状回復費用を差し引いて返金される。",
        "category": "rental",
        "synonyms": ["保証金"],
        "examples": ["敷金2ヶ月", "敷金礼金なし"],
    },
    {
        "term": "礼金",
        "language": "ja",
        "translation": "Key Money",
        "explanation": "賃貸契約時に貸主に支払うお礼のお金。返金されない。",
        "category": "rental",
        "synonyms": [],
        "examples": ["礼金1ヶ月", "礼金なし物件"],
    },
    {
        "term": "2LDK",
        "language": "ja",
        "translation": "2 Bedrooms + Living/Dining/Kitchen",
        "explanation": "リビング・ダイニング・キッチンと2つの部屋がある間取り。",
        "category": "layout",
        "synonyms": [],
        "examples": ["2LDK 70㎡", "広々2LDK"],
    },
    {
        "term": "駅近",
        "language": "ja",
        "translation": "Near Station",
        "explanation": "駅から徒歩圏内（通常5-10分以内）の物件。通勤・通学に便利。",
        "category": "location",
        "synonyms": ["駅徒歩圏内", "駅チカ"],
        "examples": ["駅徒歩5分", "駅近物件"],
    },
    {
        "term": "南向き",
        "language": "ja",
        "translation": "South-Facing",
        "explanation": "バルコニーやメインの窓が南向きの物件。日当たりが良い。",
        "category": "property_info",
        "synonyms": [],
        "examples": ["南向きバルコニー", "全室南向き"],
    },
    {
        "term": "オートロック",
        "language": "ja",
        "translation": "Auto-Lock",
        "explanation": "建物の玄関が自動でロックされるシステム。セキュリティが高い。",
        "category": "facilities",
        "synonyms": [],
        "examples": ["オートロック完備", "オートロック付き"],
    },
    {
        "term": "ペット可",
        "language": "ja",
        "translation": "Pets Allowed",
        "explanation": "ペット（犬・猫など）の飼育が可能な物件。",
        "category": "conditions",
        "synonyms": ["ペット飼育可", "ペットOK"],
        "examples": ["小型犬可", "猫2匹まで可"],
    },
    {
        "term": "初期費用",
        "language": "ja",
        "translation": "Initial Cost",
        "explanation": "入居時に必要な費用の総額。敷金・礼金・仲介手数料・前家賃などを含む。",
        "category": "cost",
        "synonyms": ["入居費用"],
        "examples": ["初期費用50万円", "初期費用を抑えたい"],
    },
    {
        "term": "仲介手数料",
        "language": "ja",
        "translation": "Brokerage Fee",
        "explanation": "不動産会社に支払う手数料。通常は家賃の1ヶ月分+税。",
        "category": "cost",
        "synonyms": ["仲介料"],
        "examples": ["仲介手数料無料", "仲介手数料半額"],
    },
    # English terms
    {
        "term": "Security Deposit",
        "language": "en",
        "translation": "敷金",
        "explanation": "Money paid to the landlord at the start of a tenancy, refunded after deducting repair costs.",
        "category": "rental",
        "synonyms": ["Deposit"],
        "examples": ["2 months security deposit", "No deposit required"],
    },
    {
        "term": "Key Money",
        "language": "en",
        "translation": "礼金",
        "explanation": "Non-refundable money paid to the landlord as a gift in Japanese rental contracts.",
        "category": "rental",
        "synonyms": ["Gift Money"],
        "examples": ["1 month key money", "No key money"],
    },
    # Vietnamese terms
    {
        "term": "Tiền đặt cọc",
        "language": "vi",
        "translation": "Security Deposit / 敷金",
        "explanation": "Số tiền trả cho chủ nhà khi bắt đầu thuê, sẽ được hoàn lại sau khi trừ chi phí sửa chữa.",
        "category": "rental",
        "synonyms": ["Tiền cọc"],
        "examples": ["Đặt cọc 2 tháng", "Không cần đặt cọc"],
    },
]


async def seed_glossary() -> None:
    """Seed glossary terms into the database."""
    settings = get_settings()

    # Create async engine
    engine = create_async_engine(str(settings.database_url), echo=True)

    # Create async session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        repo = GlossaryRepository(session)

        print(f"Seeding {len(GLOSSARY_TERMS)} glossary terms...")

        for term_data in GLOSSARY_TERMS:
            # Check if term already exists
            existing = await repo.get_by_term(
                term=term_data["term"],
                language=term_data["language"],
            )

            if existing:
                print(f"  ⏭️  Skipping existing term: {term_data['term']} ({term_data['language']})")
                continue

            # Create new term
            await repo.create(**term_data)
            print(f"  ✅ Created: {term_data['term']} ({term_data['language']})")

    await engine.dispose()
    print("\n✅ Glossary seeding complete!")


if __name__ == "__main__":
    asyncio.run(seed_glossary())
