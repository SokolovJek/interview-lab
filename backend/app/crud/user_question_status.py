from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from app.models.user_question_status import UserQuestionStatus
from app.schemas.user_question_status import UserQuestionStatusCreate, UserQuestionStatusUpdate


def create_status(status_data: UserQuestionStatusCreate, db: Session) -> UserQuestionStatus:
    """Создание нового статуса"""
    status = UserQuestionStatus(
        user_id=status_data.user_id,
        question_id=status_data.question_id,
        status=status_data.status,
        attempts=0,
        correct=0,
        first_seen_at=datetime.now()
    )
    db.add(status)
    db.commit()
    db.refresh(status)
    return status


def get_by_user_and_question(
    user_id: int,
    question_id: int,
    db: Session
) -> Optional[UserQuestionStatus]:
    """Получение статуса по user_id и question_id"""
    return db.query(UserQuestionStatus).filter(
        UserQuestionStatus.user_id == user_id,
        UserQuestionStatus.question_id == question_id
    ).first()


def get_by_user(
    user_id: int,
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[UserQuestionStatus]:
    """Получение всех статусов пользователя"""
    return db.query(UserQuestionStatus).filter(
        UserQuestionStatus.user_id == user_id
    ).offset(skip).limit(limit).all()


def get_by_status(
    user_id: int,
    status: str,
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[UserQuestionStatus]:
    """Получение статусов пользователя по статусу"""
    return db.query(UserQuestionStatus).filter(
        UserQuestionStatus.user_id == user_id,
        UserQuestionStatus.status == status
    ).offset(skip).limit(limit).all()


def update_question_status(
    status_data: UserQuestionStatusUpdate,
    db: Session
) -> UserQuestionStatus:
    """Обновление статуса после ответа на вопрос"""
    user_id = status_data.user_id
    question_id = status_data.question_id
    new_status  = status_data.status

    status = get_by_user_and_question(user_id, question_id, db)

    is_correct = 1 if new_status  in ['passed'] else 0

    if not status:
        # Создаем новую запись
        status_data = UserQuestionStatusCreate(
            user_id=user_id,
            question_id=question_id,
            status=new_status
        )
        status = create_status(status_data, db)
        status.attempts = 1
        status.correct = 1 if is_correct else 0
        status.last_attempt_at = datetime.now()
    else:
        # Обновляем существующую
        status.attempts += 1
        if is_correct:
            status.correct += 1
        status.status = new_status
        status.last_attempt_at = datetime.now()

    db.add(status)
    db.commit()
    db.refresh(status)
    return status


def get_user_stats(user_id: int, db: Session) -> dict:
    """Получение статистики пользователя"""
    statuses = get_by_user(user_id, db)

    total = len(statuses)
    passed = sum(1 for s in statuses if s.status == "passed")
    repeat = sum(1 for s in statuses if s.status == "repeat")
    in_progress = sum(1 for s in statuses if s.status == "in_progress")
    not_passed = sum(1 for s in statuses if s.status == "not_passed")

    return {
        "total_questions": total,
        "passed": passed,
        "repeat": repeat,
        "in_progress": in_progress,
        "not_passed": not_passed,
        "success_rate": round((passed / total * 100) if total > 0 else 0, 2)
    }
