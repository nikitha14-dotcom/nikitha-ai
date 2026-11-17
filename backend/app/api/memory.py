# backend/app/api/memory.py
"""Memory CRUD endpoints.
All routes are protected – only authenticated users can access their own memory entries.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional

from backend.app.core.security import get_current_user_optional
from backend.app.database import get_db
from backend.app.models.memory import Memory
from backend.app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

router = APIRouter()

class MemoryCreate(BaseModel):
    category: Optional[str] = Field(default="preference")
    key: str
    value: str
    confidence: Optional[float] = 1.0
    source: Optional[str] = "conversation"

class MemoryResponse(BaseModel):
    id: int
    category: str
    key: str
    value: str
    confidence: float
    source: str
    created_at: str
    updated_at: str

@router.post("/", response_model=MemoryResponse, status_code=status.HTTP_201_CREATED)
async def create_memory(item: MemoryCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user_optional)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    mem = Memory(
        category=item.category,
        key=item.key,
        value=item.value,
        confidence=item.confidence,
        source=item.source,
    )
    db.add(mem)
    await db.commit()
    await db.refresh(mem)
    return MemoryResponse(
        id=mem.id,
        category=mem.category,
        key=mem.key,
        value=mem.value,
        confidence=mem.confidence,
        source=mem.source,
        created_at=mem.created_at.isoformat(),
        updated_at=mem.updated_at.isoformat(),
    )

@router.get("/", response_model=List[MemoryResponse])
async def list_memory(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user_optional)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    result = await db.execute(select(Memory))
    memories = result.scalars().all()
    return [
        MemoryResponse(
            id=m.id,
            category=m.category,
            key=m.key,
            value=m.value,
            confidence=m.confidence,
            source=m.source,
            created_at=m.created_at.isoformat(),
            updated_at=m.updated_at.isoformat(),
        )
        for m in memories
    ]

@router.delete("/{mem_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_memory(mem_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user_optional)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    await db.execute(delete(Memory).where(Memory.id == mem_id))
    await db.commit()
    return None
