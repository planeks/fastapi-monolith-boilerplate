FROM --platform=linux/amd64 python:3.13-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

ENV PYTHONPATH=/app

WORKDIR /app

COPY uv.lock pyproject.toml /app/

RUN uv sync --frozen --no-dev

COPY . /app

ENTRYPOINT ["scripts/start.sh"]
