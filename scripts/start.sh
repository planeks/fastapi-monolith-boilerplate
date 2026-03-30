#!/bin/bash
echo "Applying database migrations"
uv run alembic upgrade head

# If a command was passed (e.g. "uv run pytest"), run it instead of the server
if [ $# -gt 0 ]; then
    exec "$@"
fi

echo "Starting FastAPI application"
exec uv run python src/app.py
