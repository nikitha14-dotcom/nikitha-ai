# backend/app/api/auth.py
"""Authentication routes: register, login, get current user.
All routes are mounted under /api/v1/auth via the api_router.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.config import settings
from backend.app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user_optional,
)
from backend.app.database import get_db
from backend.app.models.user import User

router = APIRouter()

class RegisterSchema(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=30)
    password: str = Field(..., min_length=8)

class LoginSchema(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterSchema, db: AsyncSession = Depends(get_db)):
    # Ensure email/username uniqueness
    result = await db.execute(select(User).where(User.email == payload.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")
    result = await db.execute(select(User).where(User.username == payload.username))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed = get_password_hash(payload.password)
    new_user = User(
        email=payload.email,
        username=payload.username,
        hashed_password=hashed,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    access_token = create_access_token({"sub": new_user.username})
    return {"access_token": access_token}

@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == payload.username))
    user = result.scalars().first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token}

@router.get("/me")
async def read_current_user(user: User = Depends(get_current_user_optional)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "is_active": user.is_active,
    }
