# Author: Sanidayal Gupta
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Autonomous BFSI Fraud & AML Shield API"
    AUTHOR: str = "Sanidayal Gupta"
    ENVIRONMENT: str = "development"
    PORT: int = 8000

    GEMINI_API_KEY: str = "mock-key-for-local-dev"
    GEMINI_MODEL: str = "gemini-2.5-flash"

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/bfsi_fraud_guard_db"
    REDIS_URL: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
