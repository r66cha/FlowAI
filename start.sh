#!/bin/sh

# Alembic миграции
python -m alembic upgrade head

# Celery worker и flower
python -m celery -A src.core.repository.services.celery.app.celery_app worker --loglevel=info &
python -m celery -A src.core.repository.services.celery.app.celery_app flower --port=5555 &

# Запуск FastAPI через uvicorn
python main.py

wait