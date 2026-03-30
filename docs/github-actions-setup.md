# GitHub Actions Setup

After provisioning a server with `./scripts/provision-server.sh`, GitHub Actions needs:
1. SSH access to the server
2. The server's IP address
3. Proper directory structure and permissions

The provisioning script configures items 2 and 3 automatically. You need to add the SSH credentials to GitHub.

## Workflow files

```
.github/workflows/
  ci.yml                    # CI: lint, migration check, tests
  deploy-reusable.yml       # Shared deploy logic
  dev_deploy.yml            # Deploy on push to develop
  staging_deploy.yml        # Deploy on push to staging (CI gate)
  production_deploy.yml     # Deploy on push to main (CI gate + approval)
```

## Set up environments

In your GitHub repository:

1. Go to Settings > Environments
2. Create three environments: `dev`, `staging`, `production`

### Production environment protection

For the `production` environment:
1. Click on `production`
2. Enable "Required reviewers"
3. Add team members who should approve production deployments

## Configure secrets

For each environment, add the required secrets.

### Development (`dev`)

Go to Settings > Environments > dev > Secrets

- `DEV_HOST` -- development server IP or hostname
- `DEV_SSH_KEY` -- SSH private key for accessing the dev server
- `DEV_SSH_USER` (optional) -- SSH username, defaults to `appuser`

### Staging (`staging`)

Go to Settings > Environments > staging > Secrets

- `STAGING_HOST` -- staging server IP or hostname
- `STAGING_SSH_KEY` -- SSH private key for accessing the staging server
- `STAGING_SSH_USER` (optional) -- SSH username, defaults to `appuser`

### Production (`production`)

Go to Settings > Environments > production > Secrets

- `PROD_HOST` -- production server IP or hostname
- `PROD_SSH_KEY` -- SSH private key for accessing the production server
- `PROD_SSH_USER` (optional) -- SSH username, defaults to `appuser`

### Generating SSH keys

Make sure to not use a passphrase for the key.

```bash
# Generate a new SSH key pair
ssh-keygen -t ed25519 -C "github-actions" -f github_actions_key -N ""

# Copy the public key to your server
ssh-copy-id -i github_actions_key.pub appuser@your-server

# Copy the private key content to GitHub Secrets
cat github_actions_key
```

## How deployments work

### Development

Trigger: push to `develop` branch

1. Deploys to dev server using `compose.dev.yml`
2. Runs database migrations via entrypoint

```bash
git push origin develop
```

Or use Actions > Deploy to Development > Run workflow

### Staging

Trigger: push to `staging` branch

1. Runs CI tests
2. Deploys to staging server using `compose.prod.yml`
3. Runs database migrations via entrypoint

```bash
git push origin staging
```

### Production

Trigger: push to `main` branch

1. Runs CI tests
2. Requires environment approval
3. Deploys to production server using `compose.prod.yml`
4. Runs database migrations via entrypoint

```bash
git push origin main
```

## Branch strategy

```
develop  -> Development environment
   |
staging  -> Staging environment (merge develop here)
   |
 main    -> Production environment (merge staging here)
```

## Monitoring deployments

### Server health check

```bash
ssh -i <your-key> <user>@<server_ip> "bash ~/projects/fastapi_app/scripts/health-check.sh"
```

### View workflow runs

1. Go to the Actions tab in your repository
2. Select a workflow from the left sidebar
3. Click on a specific run to see details

## Troubleshooting

### FastAPI container fails to start

Common causes:

1. **Missing or invalid `.env` file**

   ```
   [ERROR] .env file not found!
   [ERROR] SECRET_KEY is not configured in .env file!
   ```

   Fix:
   ```bash
   ssh appuser@your-server
   cd ~/projects/fastapi_app
   cp .env.example .env
   nano .env
   # Fill in SECRET_KEY, POSTGRES_PASSWORD, etc.
   ```

2. **Placeholder values in `.env`**

   Required values:
   - `SECRET_KEY` -- generate with: `python3 -c 'import secrets; print(secrets.token_urlsafe(64))'`
   - `POSTGRES_PASSWORD` -- a secure database password

### "Permission denied (publickey)" during deployment

1. Check that the public key is in `authorized_keys` on the server
2. Check that the GitHub Secret has the correct private key (starts with `-----BEGIN OPENSSH PRIVATE KEY-----`)
3. Check the SSH username -- workflows default to `appuser`. If your server uses `ubuntu`, set the `*_SSH_USER` secret.

### General deployment failures

1. Check the workflow logs in the Actions tab
2. SSH into the server and check container logs:
   ```bash
   cd ~/projects/fastapi_app
   docker compose -f compose.dev.yml logs fastapi
   docker compose -f compose.dev.yml ps -a
   ```
3. Verify secrets are correctly set in GitHub
4. Check that all required environment variables are set in `.env`

## Security best practices

- Never commit secrets or SSH keys to the repository
- Use environment-specific secrets
- Rotate SSH keys regularly
- Enable branch protection rules for `main` and `staging`
- Require pull request reviews before merging
- Use required reviewers for production deployments

---

Related:
- [Automated provisioning](deployment_automated.md)
- [Manual deployment](deployment_manual.md)
- [SSH key setup](ssh-key-setup.md)
