FROM python:3.13-slim

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml ./
COPY uv.lock ./

RUN uv sync --frozen --no-dev

COPY . .

CMD uv run alembic upgrade head && uv run main.py