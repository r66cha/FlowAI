"""Celery app module."""

# -- Imports

from celery import Celery


# -- Exports

__all__ = ["celery_app"]

# --

TASKS_DIR = "src.core.repository.tasks"

# Можно также использовать Redis в качестве брокера
celery_app = Celery(
    "my_app",
    broker="amqp://guest:guest@rabbitmq:5672//",
    include=[TASKS_DIR],
    backend=None,
    broker_connection_retry_on_startup=True,
)
