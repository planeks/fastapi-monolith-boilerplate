# Code Quality

This project uses automated linting, formatting, and security scanning.

## Dependency management

This project uses [uv](https://docs.astral.sh/uv/) to manage Python dependencies.
All dependencies are declared in `pyproject.toml` and locked in `uv.lock`.

### Adding a dependency

```bash
uv add <package>
```

To pin a specific version:

```bash
uv add "sqlalchemy>=2.0,<3.0"
```

### Adding a dev dependency

```bash
uv add --group dev <package>
```

### Updating dependencies

```bash
uv lock --upgrade-package <package>   # update a specific package
uv lock --upgrade                     # update all packages
```

### Removing a dependency

```bash
uv remove <package>
```

> Always commit both `pyproject.toml` and `uv.lock` after making changes.
> After adding or removing dependencies, rebuild the Docker image: `docker compose -f compose.dev.yml build fastapi`.

## Tools

- **Ruff** handles both linting and formatting. Configuration lives in `pyproject.toml` under `[tool.ruff]`.
- **pip-audit** scans Python dependencies for known vulnerabilities in CI.

## Running locally

```bash
uv run ruff check src/              # lint
uv run ruff check --fix src/        # lint and auto-fix
uv run ruff format src/             # format
uv run ruff format --check src/     # check formatting without changes
```

Or inside Docker:

```bash
docker compose -f compose.dev.yml exec fastapi uv run ruff check src/
docker compose -f compose.dev.yml exec fastapi uv run ruff format src/
```

## Pre-commit hooks

The project includes a `.pre-commit-config.yaml` that runs Ruff automatically before each commit. To set it up:

```bash
pip install pre-commit
pre-commit install
```

After that, every `git commit` will run the hooks on staged files. To run them manually on all files:

```bash
pre-commit run --all-files
```

## CI pipeline

The GitHub Actions CI workflow (`.github/workflows/ci.yml`) runs three jobs:

1. **Lint Python** -- Ruff check, Ruff format check, pip-audit
2. **Check Migration Conflicts** -- Verifies a single Alembic head (no conflicting migrations)
3. **Test Backend** -- Runs pytest in Docker

Staging and production deploys require CI to pass first.

## Dependabot

Dependabot (`.github/dependabot.yml`) opens monthly pull requests for:

- Python dependencies (`pip` ecosystem)
- GitHub Actions versions (`github-actions` ecosystem)
