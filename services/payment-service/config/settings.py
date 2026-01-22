from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./payments.db")
    DEBUG: bool = False
    STRIPE_API_KEY: str = "mock_key"

settings = Settings()
