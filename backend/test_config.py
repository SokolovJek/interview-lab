# test_config.py
import sys
from pathlib import Path

# Добавляем папку backend в PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

from app.core.config import settings
from app.core.database import engine
from sqlalchemy import text

print(f"ENVIRONMENT: {settings.ENVIRONMENT}")
print(f"DATABASE_URL: {settings.DATABASE_URL}")
print(f"SECRET_KEY: {settings.SECRET_KEY[:10]}... (длина: {len(settings.SECRET_KEY)})")

# Проверяем подключение к БД
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))  # 👈 ОБЕРТЫВАЕМ В text()
        print("✅ Database connection successful!")
except Exception as e:
    print(f"❌ Database connection failed: {e}")