from typing import Optional, Dict
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.hashing import Hasher


def get_user(username: str, db: Session) -> Optional[User]:
    """
    Получение пользователя из БД по email адресу

    Args:
        username: email с формы
        db: объект БД

    Returns:
        User или None, если пользователь не найден
    """
    user = db.query(User).filter(User.email == username).first()
    return user


def add_hash_to_logout(user: User, db: Session) -> str:
    """
    Добавляет хеш к данным пользователя при логине и сохраняет в БД.
    Для end-point /logout

    Args:
        user: объект пользователя
        db: объект БД

    Returns:
        Хеш для logout
    """
    hash_to_logout: str = Hasher.get_hash_to_realize_function_logout(str(user.id))
    user.hash = hash_to_logout
    db.commit()
    return hash_to_logout


def delete_hash_to_logout(user: User, db: Session) -> Dict[str, bool]:
    """
    Удаляет хеш из данных пользователя при логауте.
    Для end-point /logout

    Args:
        user: объект пользователя
        db: объект БД

    Returns:
        Словарь с результатом операции
    """
    user.hash = ''
    db.commit()
    return {'result': True}
