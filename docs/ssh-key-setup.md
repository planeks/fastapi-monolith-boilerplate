# SSH Key Setup for GitHub Actions

## Overview

The provisioning process **automatically handles SSH key creation** and provides clear instructions for adding keys to GitHub.

## Two Types of SSH Keys

### 1. GitHub Actions SSH Key (GitHub -> Server)
**Purpose:** Allows GitHub Actions to deploy to your server

- **Location:** `~/.ssh/github_actions` (on your local machine)
- **Direction:** GitHub Actions -> Your Server
- **Setup:** Automatic during provisioning

### 2. Deploy Key (Server -> GitHub)
**Purpose:** Allows your server to pull code from GitHub

- **Location:** `/home/appuser/.ssh/id_rsa` (on the server)
- **Direction:** Your Server -> GitHub Repository
- **Setup:** Automatic during provisioning

## Automatic Setup Process

When you run `provision-server.sh`:

### Step 1: SSH Key Check
The script checks if `~/.ssh/github_actions` exists on your local machine.

### Step 2: Key Creation (if needed)
If the key doesn't exist, it will:
- Generate an Ed25519 SSH key pair
- Save it at `~/.ssh/github_actions`
- Display instructions for adding it to GitHub

### Step 3: Server Configuration
The Ansible playbook automatically:
- Adds the **public key** to the server's `~/.ssh/authorized_keys`
- Configures proper permissions
- Sets up the deployment directory

## Manual Commands

If you need to manage keys manually:

### Generate SSH Key
```bash
ssh-keygen -t ed25519 -C "github-actions" -f ~/.ssh/github_actions -N ""
```

### View Private Key (for GitHub Secrets)
```bash
cat ~/.ssh/github_actions
```

### View Public Key (for server)
```bash
cat ~/.ssh/github_actions.pub
```

### Export Public Key for Provisioning
```bash
export GITHUB_ACTIONS_SSH_KEY="$(cat ~/.ssh/github_actions.pub)"
./scripts/provision-server.sh aws production YOUR_SERVER_IP
```

## GitHub Secrets Required

For each environment, you need:

| Environment | Secrets Required |
|-------------|------------------|
| Production | `PROD_HOST`, `PROD_SSH_KEY` |
| Staging | `STAGING_HOST`, `STAGING_SSH_KEY` |
| Development | `DEV_HOST`, `DEV_SSH_KEY` |

**Note:** You can use the same SSH key for all environments by copying the same private key to each secret.

## Troubleshooting

### "Permission denied (publickey)" when deploying
- Verify `PROD_SSH_KEY` contains the **entire** private key including header/footer
- Check the public key is in the server's `~/.ssh/authorized_keys`
- Verify the server user matches the deployment workflow

### Key already exists
If `~/.ssh/github_actions` already exists:
- The script will use the existing key
- Run `cat ~/.ssh/github_actions` to view the private key if needed

### Want to regenerate keys
```bash
rm ~/.ssh/github_actions ~/.ssh/github_actions.pub
./scripts/provision-server.sh aws production YOUR_SERVER_IP
```

## Security Best Practices

1. **Never commit private keys** to your repository
2. **Use different keys** for different repositories when possible
3. **Rotate keys periodically** (e.g., every 6 months)
4. **Revoke old keys** when no longer needed
5. **Use read-only deploy keys** for the server -> GitHub key

---

Related:
- [GitHub Actions setup](github-actions-setup.md)
- [Automated provisioning](deployment_automated.md)
- [Manual deployment](deployment_manual.md)
