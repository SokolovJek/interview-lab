from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.users import UserCreate, ShowUser, UserUpdate
from app.core.database import get_db
from app.models.user import User
from app.api.deps import get_current_user_from_token
from app.services.user_service import UserService


router = APIRouter()


@router.post('/register', response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Регистрация нового пользователя
    """
    return UserService.create_user(user_data=user, db=db)


@router.get('', response_model=ShowUser)
def show_current_user(
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Получение информации о текущем авторизованном пользователе
    """
    return UserService.get_current_user_info(current_user)


@router.get('/all', response_model=List[ShowUser])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Получение списка всех пользователей (только для администраторов)
    """
    return UserService.get_all_users(
        skip=skip,
        limit=limit,
        current_user=current_user,
        db=db
    )


@router.get('/{id_user}', response_model=ShowUser)
def show_user_by_id(
    id_user: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Получение пользователя по ID (только для владельца или администратора)
    """
    return UserService.get_user_by_id(
        user_id=id_user,
        current_user=current_user,
        db=db
    )


@router.put('/{id_user}', response_model=ShowUser)
def update_user(
    id_user: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Обновление данных пользователя (только для владельца или администратора)
    """
    update_data = user_update.model_dump(exclude_unset=True)

    return UserService.update_user(
        user_id=id_user,
        user_data=update_data,
        current_user=current_user,
        db=db
    )


@router.delete('/{id_user}')
def delete_user(
    id_user: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Удаление пользователя (только для администраторов)
    """
    UserService.delete_user(
        user_id=id_user,
        current_user=current_user,
        db=db
    )
    return {"message": f"Пользователь с id {id_user} успешно удален"}
