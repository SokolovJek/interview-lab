from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.auth_service import AuthService
from app.api.v1.route_authenticated import oauth2_scheme
from app.models.user import User


def get_current_user_from_token(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Зависимость для получения текущего пользователя
    Используется в защищенных эндпоинтах
    """
    user = AuthService.get_current_user(token, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Не удалось подтвердить учетные данные'
        )
    return user
