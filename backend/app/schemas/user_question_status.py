from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, Literal


class UserQuestionStatusBase(BaseModel):
    status: Literal["passed", "not_passed", "repeat"] = "not_passed"


class UserQuestionStatusCreate(UserQuestionStatusBase):
    user_id: int
    question_id: int


class UserQuestionStatusUpdate(BaseModel):
    status: Optional[Literal["passed", "not_passed", "repeat"]] = None


class UserQuestionStatusResponse(UserQuestionStatusBase):
    id: int
    user_id: int
    question_id: int
    attempts: int
    correct: int
    last_attempt_at: Optional[datetime]
    first_seen_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuestionAnswerRequest(BaseModel):
    """Запрос на проверку ответа"""
    question_id: int
    user_answer: str = Field(..., min_length=1)


class QuestionAnswerResponse(BaseModel):
    """Ответ на проверку"""
    is_correct: bool
    correct_answer: Optional[str] = None
    attempts: int
    status: str
    message: str
