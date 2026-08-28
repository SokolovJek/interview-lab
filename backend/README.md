### Для запуска приложения:
1) создаем виртуальное окружение: `python3 -m venv env`
2) `pip install -r requirements.txt`
3) настраиваем базу данных в файле .env:
   ```
   # Для PostgreSQL
   DATABASE_URL=postgresql://user:password@localhost:5432/db_name

   # Для SQLite
   DATABASE_URL=sqlite:///./sql_app.db
   ```

4) Запуск приложения
   ```
   # 1. Убедись, что PostgreSQL запущен
   psql -U postgres -d interview_lab -c "SELECT 1"

   # 2. Создай БД (если еще нет)
   psql -U postgres -c "CREATE DATABASE interview_lab;"

   # 3. Перейди в папку backend
   cd backend

   # 4. Активируй виртуальное окружение
   .\env\Scripts\activate

   # 5. Проверь настройки .env
   # DATABASE_URL=postgresql://user_name:password@localhost:5432/interview_lab

   # 6. Создай миграцию (если еще нет)
   alembic revision --autogenerate -m "Initial migration"

   # 7. Примени миграцию (создаст таблицы)
   alembic upgrade head

   # 8. Проверь таблицы
   psql -U user_name -d interview_lab -c "\dt"

   # 9. Запусти приложение
   uvicorn app.main:app --reload
   ```

### Проверка запуска БД:
```
cd backend
python test_config.py
```

### Для запуска тестов:
```
cd backend
pytest tests/
```

Для просмотра всех доступных end-point:
1) запускаем приложение
2) переходим по ссылке http://127.0.0.1:8000/docs

### Реализация logout на стороне backend:
Используется хеш, который сохраняется в БД и в токене:
- При входе: создается хеш → сохраняется в БД и в JWT токен
- При выходе: хеш удаляется из БД
- При проверке авторизации: сравнивается хеш из токена с хешем в БД


### Иерархия папок:
```
backend/
├── .env                      # Креды (не пушим в Git!)
├── .env.example              # Пример кредов
├── .gitignore
├── Dockerfile
├── requirements.txt
├── alembic/                  # Папка для миграций БД
│   └── versions/
├── app/
│   ├── __init__.py
│   ├── main.py               # Точка входа
│   │
│   ├── api/                  # Все эндпоинты
│   │   ├── __init__.py
│   │   ├── deps.py           # Зависимости (получение текущего юзера)
│   │   └── v1/               # Версионирование API (v1)
│   │       ├── __init__.py
│   │       ├── router.py     # Сборщик всех роутеров для v1
│   │       ├── auth.py       # Логин, регистрация, logout
│   │       ├── users.py      # CRUD для пользователей
│   │       └── question.py  # Эндпоинты для работы с вопросами
│   │
│   ├── core/                 # Ядро приложения
│   │   ├── __init__.py
│   │   ├── config.py         # Настройки из .env (Pydantic)
│   │   ├── security.py       # JWT токены (общее)
│   │   ├── database.py       # Engine, SessionLocal, get_db()
│   │   └── hashing.py        # Хеширование паролей (только bcrypt)
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py       # Логин, logout, refresh
│   │   ├── question_service.py   # Работа с вопросами
│   │   └── user_service.py       # Работа с пользователями
│   │
│   ├── models/               # SQLAlchemy модели
│   │   ├── __init__.py
│   │   ├── base.py           # Базовый класс с id, created_at
│   │   ├── user.py
│   │   ├── question.py
│   │   └── user_question_status.py
│   │
│   ├── schemas/              # Pydantic схемы
│   │   ├── __init__.py
│   │   ├── token.py
│   │   ├── user.py
│   │   ├── question.py
│   │   ├── user_question_status.py
│   │   └── question.py
│   │
│   ├── crud/                 # Работа с БД
│   │   ├── __init__.py
│   │   ├── base.py           # Базовый CRUD класс
│   │   ├── user.py
│   │   ├── user_question_status.py
│   │   └── question.py
│   │
│   └── utils/                # Вспомогательные функции
│       ├── __init__.py
│       └── email.py
│
├── tests/                    # Тесты
│   ├── __init__.py
│   ├── conftest.py           # Фикстуры
│   ├── test_auth.py
│   └── test_questions.py
│
└── scripts/                  # Вспомогательные скрипты
    ├── create_superuser.py

```

### Миграции
```
# 1. Изменил модели (добавил/удалил колонки)
# 2. Создаешь миграцию
alembic revision --autogenerate -m "Added new column"

# 3. Проверяешь миграцию (открываешь файл *_initial_migration.py)
# 4. Применяешь
alembic upgrade head

# 5. Запускаешь приложение
uvicorn app.main:app --reload
```

### Создать Суперпользователя
```
cd backend
python scripts/create_superuser.py
```

### Полезные команды:
```
# Откат на одну миграцию
alembic downgrade -1

# Откат к началу (удалить все таблицы)
alembic downgrade base

# Проверка кода (flake8)
flake8 app/ --max-line-length=88

# Форматирование (black)
black app/
```