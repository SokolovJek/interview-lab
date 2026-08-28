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
