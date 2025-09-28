docker build:
	docker compose up --build -d

alembic-revision:
	alembic revision --autogenerate -m "$(m)"

alembic-upgrade:
	alembic upgrade head

celery:
	celery --app src.core.repository.services.celery.app worker --pool threads --loglevel INFO

flower:
	celery --app src.core.repository.services.celery.app flower

run:
	uv run main.py




