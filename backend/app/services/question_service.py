from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.question import QuestionCreate, QuestionUpdate, QuestionAnswerResponse
from app.crud.question import (
    create_question as crud_create_question,
    get_question as crud_get_question,
    get_all_questions as crud_get_all_questions,
    get_random_questions as crud_get_random_questions,
    update_question as crud_update_question,
    delete_question as crud_delete_question,
)
from app.crud.user_question_status import (
    update_status_after_answer,
    get_user_stats as crud_get_user_stats,
)


class QuestionService:
    """Сервис для работы с вопросами"""

    @staticmethod
    def create_question(question_data: QuestionCreate, db: Session):
        """Создание нового вопроса"""
        return crud_create_question(question_data, db)

    @staticmethod
    def get_question(question_id: int, db: Session):
        """Получение вопроса по ID"""
        question = crud_get_question(question_id, db)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Вопрос с id {question_id} не найден"
            )
        return question

    @staticmethod
    def get_all_questions(
        skip: int = 0,
        limit: int = 100,
        db: Session = None
    ) -> List:
        """Получение всех вопросов"""
        return crud_get_all_questions(db, skip=skip, limit=limit)

    @staticmethod
    def get_random_questions(limit: int = 10, db: Session = None) -> List:
        """Получение случайных вопросов"""
        return crud_get_random_questions(db, limit=limit)

    @staticmethod
    def update_question(
        question_id: int,
        question_data: QuestionUpdate,
        db: Session
    ):
        """Обновление вопроса"""
        # Проверяем, существует ли вопрос
        question = crud_get_question(question_id, db)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Вопрос с id {question_id} не найден"
            )

        updated = crud_update_question(question_id, question_data, db)
        return updated

    @staticmethod
    def delete_question(question_id: int, db: Session) -> bool:
        """Удаление вопроса"""
        # Проверяем, существует ли вопрос
        question = crud_get_question(question_id, db)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Вопрос с id {question_id} не найден"
            )

        return crud_delete_question(question_id, db)

    @staticmethod
    def get_user_stats(user_id: int, db: Session) -> Dict[str, Any]:
        """Получение статистики пользователя"""
        return crud_get_user_stats(user_id, db)
