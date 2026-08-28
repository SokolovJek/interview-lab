# scripts/create_superuser.py
import sys
from pathlib import Path

# Добавляем путь к проекту
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import SessionLocal
from app.core.hashing import Hasher
from app.models.user import User


def create_superuser():
    db = SessionLocal()

    try:
        # Проверяем, существует ли уже суперпользователь
        existing = db.query(User).filter(User.email == "superuser@example.com").first()
        if existing:
            print("⚠️ Суперпользователь уже существует!")
            return

        # Создаем суперпользователя
        superuser = User(
            username="superuser",
            email="superuser@example.com",
            hashed_password=Hasher.get_password_hash("superuser_password_123"),
            is_active=True,
            is_superuser=True,
            hash=""
        )

        db.add(superuser)
        db.commit()
        db.refresh(superuser)

        print(f"✅ Суперпользователь создан!")
        print(f"   ID: {superuser.id}")
        print(f"   Email: {superuser.email}")
        print(f"   Username: {superuser.username}")
        print(f"   Пароль: superuser_password_123")

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_superuser()
