from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Database - PostgreSQL for production
    database_url: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/insurance_rag_db")
    vector_database_url: str = os.getenv("VECTOR_DATABASE_URL", os.getenv("DATABASE_URL", "postgresql://user:password@localhost/insurance_rag_db"))
    
    # JWT
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-for-development-only-change-this-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Google Gemini API
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "your-gemini-api-key-here")
    
    # Admin credentials
    admin_username: str = os.getenv("ADMIN_USERNAME", "admin")
    admin_password: str = os.getenv("ADMIN_PASSWORD", "admin123")
    
    # CORS
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    class Config:
        env_file = ".env"


settings = Settings()
