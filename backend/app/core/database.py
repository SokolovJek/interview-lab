from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

from app.core.config import settings


# Выбор БД в зависимости от окружения
if settings.ENVIRONMENT == "testing":
    # Для тестов используем SQLite в памяти
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False
    )
else:
    # Для разработки/продакшена используем PostgreSQL
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        echo=settings.DB_ECHO
    )


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """
    Зависимость для получения сессии БД.
    Используется в эндпоинтах через Depends(get_db).
    При тестировании переопределяется через dependency_overrides.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
