from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

from app.models.question import Question
from app.schemas.question import QuestionCreate, QuestionUpdate


def create_question(question_data: QuestionCreate, db: Session) -> Question:
    """Создание нового вопроса"""
    question = Question(
        question=question_data.question,
        answer=question_data.answer,
        difficulty=question_data.difficulty,
        tag=question_data.tag,
        category=question_data.category
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def get_question(question_id: int, db: Session) -> Optional[Question]:
    """Получение вопроса по ID"""
    return db.query(Question).filter(Question.id == question_id).first()


def get_all_questions(db: Session, skip: int = 0, limit: int = 100) -> List[Question]:
    """Получение всех вопросов с пагинацией"""
    return db.query(Question).offset(skip).limit(limit).all()


def get_random_questions(db: Session, limit: int = 10) -> List[Question]:
    """Получение случайных вопросов"""
    return db.query(Question).order_by(func.random()).limit(limit).all()


def update_question(
    question_id: int,
    question_data: QuestionUpdate,
    db: Session
) -> Optional[Question]:
    """Обновление вопроса"""
    question = get_question(question_id, db)
    if question:
        update_data = question_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(question, key):
                setattr(question, key, value)
        db.commit()
        db.refresh(question)
    return question


def delete_question(question_id: int, db: Session) -> bool:
    """Удаление вопроса"""
    question = get_question(question_id, db)
    if question:
        db.delete(question)
        db.commit()
        return True
    return False
