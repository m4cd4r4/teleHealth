from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    PROJECT_NAME: str = "Exercise Service"
    DEBUG: bool = False
    API_PREFIX: str = "/api/v1"

    # Database settings
    DATABASE_URL: str

    # JWT settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        # Load settings from a .env file if present
        env_file = ".env"
        env_file_encoding = 'utf-8'

@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()

# Expose settings instance for easy import
settings = get_settings()
