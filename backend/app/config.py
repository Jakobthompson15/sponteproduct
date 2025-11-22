"""
Application configuration management using Pydantic Settings.
Loads environment variables from .env file.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Supabase Configuration
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_KEY: str
    DATABASE_URL: str

    # Application Settings
    SECRET_KEY: str
    ENVIRONMENT: str = "development"
    API_V1_PREFIX: str = "/api"

    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379"

    # Anthropic API (optional for now)
    ANTHROPIC_API_KEY: str = ""

    # Resend API (Email Service)
    RESEND_API_KEY: str

    # Clerk Configuration
    CLERK_PUBLISHABLE_KEY: str = ""
    CLERK_SECRET_KEY: str = ""

    # Google OAuth Configuration
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/oauth/google/callback"

    # CORS Settings
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """Convert comma-separated CORS origins to list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


# Global settings instance
settings = Settings()
