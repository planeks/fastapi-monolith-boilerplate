# Running the Project Without Docker

## 1. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or see the [uv installation docs](https://docs.astral.sh/uv/getting-started/installation/).

## 2. Install dependencies

```bash
uv sync
```

This creates a `.venv` directory and installs all dependencies.

## 3. Configure environment variables

Copy the environment template and fill in the values:

```bash
cp .env.example .env
```

Update database connection settings to point to your local PostgreSQL instance:

```shell
POSTGRES_DB=boilerplate
POSTGRES_USER=boilerplate
POSTGRES_PASSWORD=boilerplate
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
SECRET_KEY="<generate-a-secret-key>"
APP_HOST=localhost
APP_PORT=8000
APP_RELOAD=false
API_PREFIX="/api"
CORS_ORIGINS="http://localhost,http://localhost:8000"
```

## 4. Set up PostgreSQL

Install and start PostgreSQL locally. Create a database matching your `.env` configuration:

```bash
createdb boilerplate
```

## 5. Run database migrations

```bash
uv run alembic upgrade head
```

## 6. Start the application

```bash
uv run python src/app.py
```

The API docs will be available at http://localhost:8000/docs

## 7. Run tests

```bash
uv run pytest
```

## 8. Run linting

```bash
uv run ruff check src/           # lint
uv run ruff check --fix src/     # lint and auto-fix
uv run ruff format src/          # format
```

---

**Note:** Ensure PostgreSQL is running and accessible with the credentials in your `.env` file.
