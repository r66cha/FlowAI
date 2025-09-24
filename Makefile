docker-build:
	docker compose up --build -d

alembic-revision:
	alembic revision --autogenerate -m "$(m)"

alembic-upgrade:
	alembic upgrade head


run:
	uv run main.py
