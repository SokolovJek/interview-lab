from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, Literal


class UserQuestionStatusBase(BaseModel):
    """Базовый класс с общим полем status"""
    status: Literal["passed", "not_passed", "repeat", "in_progress"] = "not_passed"


class UserQuestionStatusCreate(UserQuestionStatusBase):
    """Создание записи в БД"""
    user_id: int
    question_id: int

class UserQuestionStatusUpdate(BaseModel):
    """Обновление статуса в БД (все поля обязательны)"""
    user_id: int
    question_id: int
    status: Literal["passed", "not_passed", "repeat", "in_progress"]

class UserQuestionStatusUpdateRequest(BaseModel):
    """Запрос от пользователя (без user_id)"""
    question_id: int
    status: Literal["passed", "not_passed", "repeat", "in_progress"]

class UserQuestionStatusResponse(UserQuestionStatusBase):
    """Ответ API"""
    id: int
    user_id: int
    question_id: int
    attempts: int
    correct: int
    last_attempt_at: Optional[datetime]
    first_seen_at: datetime

    model_config = ConfigDict(from_attributes=True)
