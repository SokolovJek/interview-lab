from sqlalchemy import Column, String, Text, DateTime, func, Enum, Index
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Question(BaseModel):
    __tablename__ = "questions"

    # Основные поля
    question = Column(Text, nullable=False, comment="Текст вопроса")
    answer = Column(Text, nullable=False, comment="Ответ на вопрос")

    # Категоризация
    tag = Column(
        String(50),
        nullable=True,
        index=True,
        comment="Группировка по тегам (Python, Web, SQL, DevOps, etc.)"
    )
    category = Column(
        String(50),
        nullable=True,
        index=True,
        comment="Подгруппа (DDL, DML, ООП, Структуры данных, Алгоритмы, etc.)"
    )

    # Метаданные
    difficulty = Column(
        Enum('easy', 'medium', 'hard', name='difficulty_level'),
        nullable=True,
        default='medium',
        comment="Уровень сложности: easy, medium, hard"
    )
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Связь со статусами пользователей
    user_statuses = relationship(
        "UserQuestionStatus",
        back_populates="question",
        cascade="all, delete-orphan"
    )

    # Составной индекс для быстрых запросов по обоим полям: тегу и группе
    __table_args__ = (
        Index('ix_questions_tag_category', 'tag', 'category'),
    )

    def __repr__(self):
        tags = f" [tag={self.tag}]" if self.tag else ""
        category = f" [{self.category}]" if self.category else ""
        return f"<Question(id={self.id}, question='{self.question[:50]}...'{tags}{category})>"
