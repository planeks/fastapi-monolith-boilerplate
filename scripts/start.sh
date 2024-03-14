#!/bin/bash
echo "Applying database migrations"
# run alembic upgrade head to apply the latest migration
poetry run alembic upgrade head
echo "Starting FastAPI application"
# run the FastAPI application
poetry run python src/app.py