import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import List

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
STORAGE_DIR.mkdir(exist_ok=True)
DOCS_DIR = STORAGE_DIR / "documents"
DOCS_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR = STORAGE_DIR / "screenshots"
SCREENSHOTS_DIR.mkdir(exist_ok=True)
RESUMES_DIR = STORAGE_DIR / "resumes"
RESUMES_DIR.mkdir(exist_ok=True)

class Settings(BaseSettings):
    PROJECT_NAME: str = "NIKITHA.AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "nikitha_ai_super_secret_jwt_key_2026_change_in_production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALGORITHM: str = "HS256"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite+aiosqlite:///{BASE_DIR}/nikitha_ai.db")
    
    # AI Providers
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    DEFAULT_PROVIDER: str = os.getenv("DEFAULT_PROVIDER", "auto")  # auto, openai, anthropic, fallback
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]
    
    # Storage
    STORAGE_PATH: Path = STORAGE_DIR
    DOCS_PATH: Path = DOCS_DIR
    SCREENSHOTS_PATH: Path = SCREENSHOTS_DIR
    RESUMES_PATH: Path = RESUMES_DIR

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
