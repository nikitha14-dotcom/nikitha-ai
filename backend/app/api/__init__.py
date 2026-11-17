# backend/app/api/__init__.py
"""Aggregate API routers.
All routes are mounted under the API version prefix defined in config (settings.API_V1_STR).
"""

from fastapi import APIRouter

# Import individual routers (they will be created in this phase)
from .auth import router as auth_router
from .chat import router as chat_router
from .memory import router as memory_router
from .tasks import router as tasks_router
from .settings import router as settings_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
api_router.include_router(memory_router, prefix="/memory", tags=["memory"])
api_router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
api_router.include_router(settings_router, prefix="/settings", tags=["settings"])
