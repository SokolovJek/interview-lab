## 📖 О проекте

**Interview Lab** — это веб-приложение для подготовки к техническим собеседованиям.
Платформа позволяет:
- ✅ Изучать вопросы с подробными ответами
- 🎯 Практиковаться в режиме "вопрос-ответ"
- 📊 Отслеживать прогресс и статистику
- 🏷️ Фильтровать вопросы по тегам и категориям

### Технологии
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, JWT, Alembic
- **Frontend**: Vue 3, Pinia, Vite
- **DevOps**: Docker, Docker Compose

## Источники данных

Вопросы и ответы для наполнения базы данных взяты из репозитория:

> **[DEBAGanov / interview_questions](https://github.com/DEBAGanov/interview_questions)**
> Огромная благодарность автору за проделанную работу! 🙌

Исходный файл: [`Python_Developer_Questions.md`](https://github.com/DEBAGanov/interview_questions/blob/main/Python_Developer_Questions.md)

---

## Установка и запуск для локальной разработки
- [`backend`](https://github.com/SokolovJek/interview-lab/blob/main/backend/README.md)

- [`frontend`](https://github.com/SokolovJek/interview-lab/blob/main/frontend/README.md)

## Запуск
```bash
# скопируйте и отредактируйте файл `.env`
cp .env.example .env

# Сборка и запуск всех контейнеров
docker-compose up -d --build
```

## **Дополнительные docker команды**

### Запуск и управление
```bash
# Сборка и запуск всех контейнеров
docker-compose up -d --build

# Просмотр статуса
docker-compose ps

# Просмотр логов всех контейнеров
docker-compose logs -f

# Просмотр логов конкретного сервиса
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### Остановка и очистка
```bash
# Остановка всех контейнеров
docker-compose down

# Остановка с удалением volumes (потеря данных в БД)
docker-compose down -v

# Остановка и удаление всех контейнеров, сетей, образов
docker-compose down --rmi all -v
```

### Работа с контейнерами
```bash
# Войти в контейнер бэкенда
docker-compose exec backend /bin/bash

# Войти в контейнер БД
docker-compose exec db psql -U postgres -d interview_lab

# Выполнить миграции
docker-compose exec backend alembic upgrade head

# Создать суперпользователя
docker-compose exec backend python scripts/create_superuser.py

# Загрузить вопросы
docker-compose exec backend python scripts/seed_questions.py --tag Python
```



## Makefile команды

Для упрощения работы с Docker добавлен Makefile. Все команды выполняются из корневой директории проекта.

### Доступные команды

```bash
# Показать все доступные команды
make help

# Запустить все сервисы
make up

# Остановить все сервисы
make down

# Пересобрать все образы
make build

# Просмотреть логи всех контейнеров
make logs

# Применить миграции базы данных
make migrate

# Загрузить вопросы в БД (с тегом python)
make seed

# Войти в контейнер бэкенда (shell)
make shell-backend

# Войти в контейнер БД (psql)
make shell-db
```
