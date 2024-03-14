FROM --platform=linux/amd64 python:3.11-bullseye

ENV PYTHONPATH /app

RUN python -m pip install poetry

WORKDIR /app

COPY poetry.lock /app
COPY pyproject.toml /app

RUN poetry install --no-root

COPY . /app

ENTRYPOINT [ "scripts/start.sh" ]
