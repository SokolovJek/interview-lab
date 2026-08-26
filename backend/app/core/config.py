from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field


class Settings(BaseSettings):
    # Настройки проекта
    PROJECT_NAME: str = "Interview Prep API"
    PROJECT_VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default="development", pattern="^(development|testing|production)$")

    # читаем DATABASE_URL из .env
    DATABASE_URL: str = Field(..., alias="DATABASE_URL")

    # JWT
    SECRET_KEY: str = Field(..., alias="SECRET_KEY", min_length=32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Настройки пула соединений
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_ECHO: bool = False

    # Указываем Pydantic где искать переменные окружения
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
