# Manual Server Deployment

This guide covers manual server setup without Ansible. For automated provisioning, see [deployment_automated.md](deployment_automated.md).

## Configure main user

Deploy the project with an unprivileged user instead of `root`.

> On AWS EC2, you already have an unprivileged user called `ubuntu` by default. If that user exists, you don't need to create another one.

Create a user (e.g., `appuser`):

```shell
adduser appuser
```

Add the user to the `sudo` group:

```bash
usermod -aG sudo appuser
```

Set up SSH key authentication. If you don't have a key yet, create one on your local machine:

```bash
ssh-keygen -t ed25519
```

Copy your public key to the server:

```bash
ssh-copy-id appuser@YOUR_SERVER_IP
```

Test key-based login:

```bash
ssh appuser@YOUR_SERVER_IP
```

## Install dependencies

Install required packages:

```bash
sudo apt install -y git wget tmux htop mc nano build-essential
```

Install Docker and Docker Compose ([official docs](https://docs.docker.com/engine/install/)):

```bash
# Add Docker's official GPG key
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Add your user to the docker group:

```bash
sudo usermod -aG docker "$USER"
```

Create the `app` group with GID 1024. This is used for non-root volume permissions:

```bash
sudo addgroup --gid 1024 app
```

> If GID 1024 is unavailable, pick a different value and update the `Dockerfile` to match.

Add your user to the group:

```bash
sudo usermod -aG app ${USER}
newgrp app
```

## Generate deploy key

Create an SSH key on the server for pulling code from the remote repository:

```bash
ssh-keygen -t ed25519
```

Show the public key:

```bash
cat ~/.ssh/id_ed25519.pub
```

Add this key to your repository's deploy keys (on GitHub: Settings > Deploy keys).

> Deploy keys grant read-only access to the repository and don't count against your user quota.

## Clone the project

Create the directory and clone:

```bash
mkdir ~/projects
cd ~/projects
git clone <git_remote_url>
```

Create the `.env` file from the template:

```shell
cp .env.example .env
```

Open `.env` and fill in production values:

```shell
POSTGRES_DB=db
POSTGRES_USER=dbuser
POSTGRES_PASSWORD=<strong-password>
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
SECRET_KEY="<generate-a-secret-key>"
APP_HOST=0.0.0.0
APP_PORT=8000
APP_RELOAD=false
API_PREFIX="/api"
CORS_ORIGINS="https://yourdomain.com"
```

> Generate strong values for `SECRET_KEY` and `POSTGRES_PASSWORD`:
> ```bash
> python3 -c 'import secrets; print(secrets.token_urlsafe(64))'
> openssl rand -base64 32
> ```

Build and start:

```bash
docker compose -f compose.dev.yml build
docker compose -f compose.dev.yml up -d
```

## Verify

Check that all containers are running:

```bash
docker compose -f compose.dev.yml ps
```

Check application logs:

```bash
docker compose -f compose.dev.yml logs -f fastapi
```

The API docs should be available at `http://YOUR_SERVER_IP:8000/docs`.

---

Related:
- [Automated provisioning](deployment_automated.md)
- [GitHub Actions setup](github-actions-setup.md)
- [Backups](backup.md)
