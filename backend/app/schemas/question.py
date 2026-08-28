from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

from app.schemas.user_question_status import UserQuestionStatusResponse


class QuestionBase(BaseModel):
    question: str = Field(..., min_length=1, description="Текст вопроса")
    answer: str = Field(..., min_length=1, description="Эталонный ответ")


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(BaseModel):
    question: Optional[str] = Field(None, min_length=1)
    answer: Optional[str] = Field(None, min_length=1)


class QuestionResponse(QuestionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuestionWithStatusResponse(QuestionResponse):
    """Вопрос с информацией о статусе пользователя"""
    user_status: Optional[UserQuestionStatusResponse] = None


# ============================================
# ДЛЯ ПРОВЕРКИ ОТВЕТОВ
# ============================================

class QuestionAnswerRequest(BaseModel):
    """Запрос на проверку ответа"""
    question_id: int = Field(..., description="ID вопроса")
    user_answer: str = Field(..., min_length=1, description="Ответ пользователя")


class QuestionAnswerResponse(BaseModel):
    """Ответ на проверку"""
    is_correct: bool = Field(..., description="Правильно ли ответил пользователь")
    correct_answer: Optional[str] = Field(None, description="Правильный ответ (если ответ неверный)")
    attempts: int = Field(..., description="Количество попыток")
    status: str = Field(..., description="Текущий статус вопроса")
    message: str = Field(..., description="Сообщение о результате")
