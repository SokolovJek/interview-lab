from sqlalchemy import Column, String, Text, DateTime, func
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Question(BaseModel):
    __tablename__ = "questions"

    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Связь со статусами пользователей
    user_statuses = relationship(
        "UserQuestionStatus",
        back_populates="question",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Question(id={self.id}, question='{self.question[:50]}...')>"
