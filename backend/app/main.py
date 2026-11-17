# backend/app/main.py
"""FastAPI application entry point for NIKITHA.AI backend.
Creates the FastAPI app, loads configuration, registers core routes, CORS, and DB init.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.api import api_router

from backend.app.database import init_db

def create_app() -> FastAPI:
    """Factory to create a FastAPI instance with configuration and middleware."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def on_startup():
        await init_db()

    @app.get("/", tags=["health"])
    async def root() -> dict:
        """Simple health check endpoint."""
        return {"status": "ok", "message": "NIKITHA.AI backend is running"}

    # Include versioned API router
    app.include_router(api_router, prefix=settings.API_V1_STR)
    return app

# Instantiate the app for ASGI servers like uvicorn.
app = create_app()
