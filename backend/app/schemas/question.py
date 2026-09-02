from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, Literal

from app.schemas.user_question_status import UserQuestionStatusResponse


class QuestionBase(BaseModel):
    question: str = Field(..., min_length=1, description="Текст вопроса")
    answer: str = Field(..., min_length=1, description="Эталонный ответ")
    difficulty: Literal['easy', 'medium', 'hard'] = "medium"
    category: Optional[str] = Field(None, min_length=1, description="Категории")
    tag: Optional[str] = Field(None, min_length=1, description="Группировка по тегам")


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(BaseModel):
    question: Optional[str] = Field(None, min_length=1)
    answer: Optional[str] = Field(None, min_length=1)
    difficulty: Optional[Literal['easy', 'medium', 'hard']] = None
    category: Optional[str]  = Field(None, min_length=1)
    tag: Optional[str]  = Field(None, min_length=1)


class QuestionResponse(QuestionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuestionWithStatusResponse(QuestionResponse):
    """Вопрос с информацией о статусе пользователя"""
    user_status: Optional[UserQuestionStatusResponse] = None
