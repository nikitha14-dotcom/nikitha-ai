import re
from typing import List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from backend.app.models.memory import Memory

# Redaction patterns for sensitive data
SENSITIVE_PATTERNS = [
    r"sk-[a-zA-Z0-9_-]{20,}",            # OpenAI keys
    r"sk-ant-[a-zA-Z0-9_-]{20,}",        # Claude keys
    r"password\s*[:=]\s*\S+",             # Passwords
    r"bearer\s+[a-zA-Z0-9_\-\.]+",       # Bearer tokens
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b.*password",
]

def redact_sensitive_info(text: str) -> str:
    cleaned = text
    for pattern in SENSITIVE_PATTERNS:
        cleaned = re.sub(pattern, "[REDACTED_CREDENTIAL]", cleaned, flags=re.IGNORECASE)
    return cleaned

class MemoryEngine:
    @staticmethod
    async def get_all_memories(db: AsyncSession, category: Optional[str] = None) -> List[Memory]:
        stmt = select(Memory).order_by(Memory.updated_at.desc())
        if category:
            stmt = stmt.where(Memory.category == category)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def save_memory(
        db: AsyncSession,
        key: str,
        value: str,
        category: str = "preference",
        confidence: float = 1.0,
        source: str = "conversation"
    ) -> Memory:
        # Check if sensitive
        safe_value = redact_sensitive_info(value)
        safe_key = redact_sensitive_info(key)

        # Check existing
        stmt = select(Memory).where(Memory.key == safe_key, Memory.category == category)
        result = await db.execute(stmt)
        existing = result.scalars().first()

        if existing:
            existing.value = safe_value
            existing.confidence = confidence
            existing.source = source
            await db.commit()
            await db.refresh(existing)
            return existing

        new_mem = Memory(
            category=category,
            key=safe_key,
            value=safe_value,
            confidence=confidence,
            source=source
        )
        db.add(new_mem)
        await db.commit()
        await db.refresh(new_mem)
        return new_mem

    @staticmethod
    async def search_memories(db: AsyncSession, query: str) -> List[Memory]:
        stmt = select(Memory).where(
            or_(
                Memory.key.ilike(f"%{query}%"),
                Memory.value.ilike(f"%{query}%"),
                Memory.category.ilike(f"%{query}%")
            )
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_context_for_prompt(db: AsyncSession, max_items: int = 15) -> str:
        memories = await MemoryEngine.get_all_memories(db)
        if not memories:
            return "No prior user memory stored yet."
        
        lines = []
        for m in memories[:max_items]:
            lines.append(f"- [{m.category.upper()}] {m.key}: {m.value}")
        return "\n".join(lines)
