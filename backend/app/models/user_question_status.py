from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, func, UniqueConstraint
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class UserQuestionStatus(BaseModel):
    __tablename__ = "user_question_status"

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)

    status = Column(
        Enum('passed', 'not_passed', 'repeat', 'in_progress', name='question_status'),
        nullable=False,
        default='not_passed',
        server_default='not_passed'
    )
    attempts = Column(Integer, nullable=False, default=0, server_default="0")
    correct = Column(Integer, nullable=False, default=0, server_default="0")

    last_attempt_at = Column(DateTime, nullable=True)
    first_seen_at = Column(DateTime, nullable=False, server_default=func.now())

    # Связи
    user = relationship("User", back_populates="question_statuses")
    question = relationship("Question", back_populates="user_statuses")

    # Уникальность пары (user_id, question_id)
    __table_args__ = (
        UniqueConstraint('user_id', 'question_id', name='uq_user_question'),
    )

    def __repr__(self):
        return f"<UserQuestionStatus(user_id={self.user_id}, question_id={self.question_id}, status='{self.status}')>"
