# backend/app/main.py
"""FastAPI application entry point for NIKITHA.AI backend.
Creates the FastAPI app, loads configuration, and registers core routes.
Additional routers can be included from other modules as the project grows.
"""

from fastapi import FastAPI
from backend.app.config import settings


def create_app() -> FastAPI:
    """Factory to create a FastAPI instance with basic configuration."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    @app.get("/", tags=["health"])
    async def root() -> dict:
        """Simple health check endpoint."""
        return {"status": "ok", "message": "NIKITHA.AI backend is running"}

    return app

# Instantiate the app for ASGI servers like uvicorn.
app = create_app()
