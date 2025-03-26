from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/auth_db"
    
    # JWT settings
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Email settings
    EMAIL_SENDER: str = "noreply@telehealth.example.com"
    SMTP_SERVER: str = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = "smtp_username"
    SMTP_PASSWORD: str = "smtp_password"
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000"]
    
    # Service settings
    SERVICE_NAME: str = "auth-service"
    SERVICE_HOST: str = "0.0.0.0"
    SERVICE_PORT: int = 8001
    
    class Config:
        env_file = ".env"

settings = Settings()
