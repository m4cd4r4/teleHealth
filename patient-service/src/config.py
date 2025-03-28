from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/patient_db"
    
    # JWT settings
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000"]
    
    # Service settings
    SERVICE_NAME: str = "patient-service"
    SERVICE_HOST: str = "0.0.0.0"
    SERVICE_PORT: int = 8002
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Auth Service URL (for token validation)
    AUTH_SERVICE_URL: str = "http://auth-service:8001"
    
    class Config:
        env_file = ".env"

settings = Settings()
