import os
from dotenv import load_dotenv
from pydantic import BaseSettings

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # General settings
    APP_NAME: str = "Santhe Payment Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./payment_service.db")
    
    # Authentication settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "secret_key_here")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Stripe settings
    STRIPE_API_KEY: str = os.getenv("STRIPE_API_KEY")
    STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET")
    
    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost",
        "http://localhost:3000",
        "https://santhe-platform.com",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
