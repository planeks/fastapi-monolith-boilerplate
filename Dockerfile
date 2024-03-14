FROM python:3.11-slim

ENV PYTHONPATH /app

RUN python -m pip install poetry

WORKDIR /app

COPY poetry.lock /app
COPY pyproject.toml /app

RUN poetry install --no-root

COPY . /app


CMD [ "poetry", "run", "python", "src/app.py" ]
# ENTRYPOINT [ "scripts/start.sh" ]
# ENTRYPOINT [ "/bin/bash" ]