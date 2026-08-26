from typing import Tuple
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.crud.users import get_user_by_email
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_session_hash
)
from app.core.hashing import Hasher


class AuthService:
    """Сервис для аутентификации"""

    @staticmethod
    def login(email: str, password: str, db: Session) -> Tuple[User, str, str]:
        """
        Аутентификация пользователя

        Returns:
            Tuple[User, str, str]: (пользователь, access_token, refresh_token)
        """
        # 1. Ищем пользователя по email
        user = get_user_by_email(email=email, db=db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль"
            )

        # 2. Проверяем пароль
        if not Hasher.verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль"
            )

        # 3. Проверяем активность
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Аккаунт деактивирован"
            )

        # 4. Генерируем hash для сессии
        session_hash = generate_session_hash()
        user.hash = session_hash
        user.last_enter = datetime.utcnow()
        db.add(user)
        db.commit()
        db.refresh(user)

        # 5. Создаем токены с session_hash
        access_token = create_access_token(
            data={"sub": user.email, "session_hash": session_hash}
        )
        refresh_token = create_refresh_token(user.email, session_hash)

        return user, access_token, refresh_token

    @staticmethod
    def refresh_tokens(refresh_token: str, db: Session) -> Tuple[str, str]:
        """Обновление токенов"""
        # 1. Декодируем refresh_token
        payload = decode_token(refresh_token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невалидный refresh токен"
            )

        # 2. Проверяем срок действия
        exp = payload.get('exp')
        if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh токен истек"
            )

        # 3. Извлекаем данные
        email = payload.get('sub')
        session_hash = payload.get('session_hash')

        if not email or not session_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невалидный refresh токен"
            )

        # 4. Проверяем пользователя
        user = get_user_by_email(email=email, db=db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь не найден"
            )

        # 5. Проверяем сессию
        if not user.hash or user.hash != session_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Сессия невалидна. Выполните повторный вход"
            )

        # 6. Создаем новые токены
        new_access_token = create_access_token(
            data={"sub": user.email, "session_hash": session_hash}
        )
        new_refresh_token = create_refresh_token(user.email, session_hash)

        return new_access_token, new_refresh_token

    @staticmethod
    def logout(user: User, db: Session) -> bool:
        """Выход пользователя"""
        user.hash = None
        db.add(user)
        db.commit()
        return True

    @staticmethod
    def get_current_user(token: str, db: Session) -> User:
        """Получение текущего пользователя по токену"""
        # 1. Декодируем токен
        payload = decode_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невалидный токен"
            )

        # 2. Извлекаем данные
        email = payload.get('sub')
        session_hash = payload.get('session_hash')

        if not email or not session_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невалидный токен"
            )

        # 3. Получаем пользователя
        user = get_user_by_email(email=email, db=db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь не найден"
            )

        # 4. Проверяем сессию
        if not user.hash or user.hash != session_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Сессия истекла. Выполните повторный вход"
            )

        # 5. Проверяем активность
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Аккаунт деактивирован"
            )

        return user
