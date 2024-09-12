# services/order-management-service/config/settings.py

from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    RABBITMQ_URL: str
    DEBUG: bool = False
    TESTING: bool = False
    SECRET_KEY: str
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
