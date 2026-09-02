.PHONY: help up down build logs migrate seed

help:
	@echo "Available commands:"
	@echo "  make up       - Start all services"
	@echo "  make down     - Stop all services"
	@echo "  make build    - Build all images"
	@echo "  make logs     - Show logs"
	@echo "  make migrate  - Run migrations"
	@echo "  make seed     - Seed questions"

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

migrate:
	docker compose exec backend alembic upgrade head

seed:
	docker compose exec backend python scripts/seed_questions.py --tag python

shell-backend:
	docker compose exec backend /bin/bash

shell-db:
	docker compose exec db psql -U ${POSTGRES_USER:-postgres} -d ${POSTGRES_DB:-interview_lab}
