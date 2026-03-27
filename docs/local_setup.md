# Local Setup with Docker

This guide shows how to start the project locally. It should become available at http://127.0.0.1:8000/

## Install Docker

For local development we recommend [Docker Desktop](https://www.docker.com/products/docker-desktop) (Windows, Linux, Mac OS).

For server installation you need Docker Engine and Docker Compose. Install on Ubuntu:

```shell
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

> For other distributions see the [official documentation](https://docs.docker.com/engine/install/).

Test Docker:

```shell
sudo systemctl status docker
```

Add your user to the `docker` group (to avoid using `sudo`):

```shell
sudo usermod -aG docker ${USER}
```

## Setup the project

Copy the environment template:

```shell
cp .env.example .env
```

Open `.env` in your editor and configure:

```shell
POSTGRES_DB=boilerplate
POSTGRES_USER=boilerplate
POSTGRES_PASSWORD=boilerplate
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
SECRET_KEY="<generate-a-secret-key>"
APP_HOST=localhost
APP_PORT=8000
APP_RELOAD=true
API_PREFIX="/api"
CORS_ORIGINS="http://localhost,http://localhost:8000"
```

Generate a secret key:

```shell
python -c 'import secrets; print(secrets.token_urlsafe(64))'
```

We recommend creating a local domain in your `/etc/hosts` file:

```
127.0.0.1   myproject.local
```

## Build and run

Build the containers:

```shell
docker compose -f compose.dev.yml build
```

Start the project in detached mode:

```shell
docker compose -f compose.dev.yml up -d
```

The API docs will be available at http://127.0.0.1:8000/docs

## Useful commands

Run bash inside the running container:

```shell
docker compose -f compose.dev.yml exec fastapi bash
```

Run a temporary container:

```shell
docker compose -f compose.dev.yml run --rm fastapi bash
```

Run Alembic migrations manually:

```shell
docker compose -f compose.dev.yml exec fastapi uv run alembic upgrade head
```

Create a new Alembic migration:

```shell
docker compose -f compose.dev.yml exec fastapi uv run alembic revision --autogenerate -m "description"
```

Run tests:

```shell
docker compose -f compose.dev.yml run --rm fastapi uv run pytest
```

View logs:

```shell
docker compose -f compose.dev.yml logs -f fastapi
```
