from datetime import datetime, timedelta
from typing import Optional
import secrets
from jose import jwt

from app.core.config import settings


def generate_session_hash() -> str:
    """
    Генерация уникального hash для сессии (logout)
    Используем secrets вместо bcrypt (быстро и безопасно)
    """
    return secrets.token_urlsafe(32)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создание access_token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(email: str, session_hash: str) -> str:
    """Создание refresh_token с session_hash"""
    expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    data = {"sub": email, "session_hash": session_hash}
    return create_access_token(data=data, expires_delta=expires)


def decode_token(token: str) -> Optional[dict]:
    """Декодирование токена"""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.JWTError:
        return None
