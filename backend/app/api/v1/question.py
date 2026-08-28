from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.api.deps import get_current_user_from_token
from app.models.user import User
from app.schemas.question import (
    QuestionCreate,
    QuestionUpdate,
    QuestionResponse,
    QuestionWithStatusResponse,
    QuestionAnswerRequest,
    QuestionAnswerResponse,
)
from app.schemas.user_question_status import UserQuestionStatusResponse
from app.services.question_service import QuestionService
from app.crud.user_question_status import (
    get_by_user_and_question,
    get_by_user,
    get_by_status,
)


router = APIRouter()


@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
def create_question(
    question_data: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """Создание нового вопроса (только для администраторов)"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только администраторы могут создавать вопросы"
        )
    return QuestionService.create_question(question_data, db)


@router.get("/", response_model=List[QuestionResponse])
def get_all_questions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """Получение всех вопросов"""
    return QuestionService.get_all_questions(skip=skip, limit=limit, db=db)


@router.get("/{question_id}", response_model=QuestionWithStatusResponse)
def get_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """Получение вопроса по ID с его статусом для пользователя"""
    question = QuestionService.get_question(question_id, db)

    user_status = get_by_user_and_question(
        user_id=current_user.id,
        question_id=question_id,
        db=db
    )

    response = QuestionWithStatusResponse.model_validate(question)
    response.user_status = user_status

    return response


@router.put("/{question_id}", response_model=QuestionResponse)
def update_question(
    question_id: int,
    question_data: QuestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """Обновление вопроса (только для администраторов)"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только администраторы могут обновлять вопросы"
        )
    return QuestionService.update_question(question_id, question_data, db)


@router.delete("/{question_id}")
def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """Удаление вопроса (только для администраторов)"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только администраторы могут удалять вопросы"
        )
    QuestionService.delete_question(question_id, db)
    return {"message": f"Вопрос с id {question_id} успешно удален"}


@router.get("/random", response_model=List[QuestionResponse])
def get_random_questions(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """Получение случайных вопросов"""
    return QuestionService.get_random_questions(limit=limit, db=db)


@router.get("/my/stats")
def get_my_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """Получение статистики текущего пользователя"""
    return QuestionService.get_user_stats(current_user.id, db)


@router.get("/my/questions", response_model=List[UserQuestionStatusResponse])
def get_my_questions(
    status: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """Получение статусов вопросов текущего пользователя"""
    if status:
        return get_by_status(
            user_id=current_user.id,
            status=status,
            db=db,
            skip=skip,
            limit=limit
        )
    return get_by_user(
        user_id=current_user.id,
        db=db,
        skip=skip,
        limit=limit
    )
