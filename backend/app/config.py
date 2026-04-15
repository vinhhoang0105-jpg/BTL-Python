"""Application configuration from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://scires:scires_secret@db:5432/scires_db"
    SECRET_KEY: str = "dev-secret-key-change-in-production-abc123xyz"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
