from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # API settings
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8003"))
    API_VERSION: str = os.getenv("API_VERSION", "v1")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "TeleHealth Appointment Service")
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/appointment_db")
    TEST_DATABASE_URL: str = os.getenv("TEST_DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/appointment_test_db")
    
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # External service URLs
    AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001/api/v1")
    PATIENT_SERVICE_URL: str = os.getenv("PATIENT_SERVICE_URL", "http://localhost:8002/api/v1")
    
    # Notification settings
    EMAIL_NOTIFICATIONS_ENABLED: bool = os.getenv("EMAIL_NOTIFICATIONS_ENABLED", "True").lower() == "true"
    SMS_NOTIFICATIONS_ENABLED: bool = os.getenv("SMS_NOTIFICATIONS_ENABLED", "False").lower() == "true"
    REMINDER_HOURS_BEFORE: List[int] = [int(h) for h in os.getenv("REMINDER_HOURS_BEFORE", "24,2").split(",")]
    
    # Calendar integration settings
    GOOGLE_CALENDAR_INTEGRATION_ENABLED: bool = os.getenv("GOOGLE_CALENDAR_INTEGRATION_ENABLED", "False").lower() == "true"
    MICROSOFT_CALENDAR_INTEGRATION_ENABLED: bool = os.getenv("MICROSOFT_CALENDAR_INTEGRATION_ENABLED", "False").lower() == "true"

    class Config:
        env_file = ".env"
        case_sensitive = True

# Create a settings instance
settings = Settings()

# API paths
API_PREFIX = f"/api/{settings.API_VERSION}"
