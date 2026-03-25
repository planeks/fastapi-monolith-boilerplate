#!/bin/bash
echo "Applying database migrations"
# run alembic upgrade head to apply the latest migration
uv run alembic upgrade head
echo "Starting FastAPI application"
# run the FastAPI application
uv run python src/app.py
