import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres-postgresql.santhe.svc.cluster.local:5432/cart_management_service_db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecret")

settings = Settings()
