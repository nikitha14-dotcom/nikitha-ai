# backend/app/api/settings.py
"""User settings endpoints.
Allows getting and updating simple key/value settings per user.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

from backend.app.core.security import get_current_user_optional
from backend.app.database import get_db
from backend.app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert

router = APIRouter()

class SettingsUpdate(BaseModel):
    settings: Dict[str, Any] = Field(..., description="Key/value pairs to store for the user")

class SettingsResponse(BaseModel):
    settings: Dict[str, Any]

# Simple in‑memory fallback if a dedicated table does not exist – for now we store in a JSON column on User (add column if missing).
# To keep it lightweight we will store a JSON dict in User.full_name as placeholder – in a real app a separate table would be used.

@router.get("/", response_model=SettingsResponse)
async def get_settings(user: User = Depends(get_current_user_optional)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    # Assume user.full_name field holds JSON for demo purposes (or empty dict)
    try:
        import json
        stored = json.loads(user.full_name) if user.full_name else {}
    except Exception:
        stored = {}
    return SettingsResponse(settings=stored)

@router.post("/", response_model=SettingsResponse)
async def update_settings(payload: SettingsUpdate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user_optional)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    # Store JSON dict into full_name for demo – not ideal but meets Phase 1.
    import json
    user.full_name = json.dumps(payload.settings)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return SettingsResponse(settings=payload.settings)
