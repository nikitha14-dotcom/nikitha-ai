# backend/app/api/chat.py
"""Chat endpoint.
Accepts a list of messages and returns a response from the AI provider service.
Falls back to the local neural engine when no provider keys are configured.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Dict, Any

from backend.app.core.security import get_current_user_optional
from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.ai.provider import ai_service

router = APIRouter()

class MessageSchema(BaseModel):
    role: str = Field(..., description="user, assistant, system")
    content: str

class ChatRequest(BaseModel):
    messages: List[MessageSchema]
    provider: str = "auto"
    model: str | None = None
    agent_name: str = "orchestrator"
    context_memories: str = ""

class ChatResponse(BaseModel):
    content: str
    model: str
    provider: str
    fallback: bool = False

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(
    payload: ChatRequest,
    db: Any = Depends(get_db),  # db not used directly now
    user: User | None = Depends(get_current_user_optional),
):
    # Enforce authentication – if no user, reject
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    # Convert pydantic messages to plain dict list for provider
    msgs = [{"role": m.role, "content": m.content} for m in payload.messages]
    reply, model_name, provider_name = await ai_service.generate_response(
        messages=msgs,
        agent_name=payload.agent_name,
        provider=payload.provider,
        model=payload.model,
        context_memories=payload.context_memories,
    )
    # ai_service returns a tuple (text, model, provider) – if fallback, provider will be "local_engine"
    fallback = provider_name == "local_engine"
    return ChatResponse(content=reply, model=model_name, provider=provider_name, fallback=fallback)
