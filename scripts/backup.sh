#!/bin/bash
# ============================================================================
# Weekly Database Backup Script
# ============================================================================
# Creates database backup inside postgres container, cleans up old backups.
#
# Usage: ./backup.sh [compose_file] [project_path] [retention_days]
# Example: ./backup.sh compose.prod.yml /home/appuser/projects/fastapi_app 30
# ============================================================================

set -euo pipefail

COMPOSE_FILE="${1:-compose.prod.yml}"
PROJECT_PATH="${2:-$(pwd)}"
RETENTION_DAYS="${3:-30}"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"; }

cd "$PROJECT_PATH"

# --- Database backup ---
log "Starting database backup..."
docker compose -f "$COMPOSE_FILE" exec -T postgres backup

log "Cleaning up database backups older than $RETENTION_DAYS days..."
docker compose -f "$COMPOSE_FILE" exec -T postgres cleanup $RETENTION_DAYS

log "Current database backups:"
docker compose -f "$COMPOSE_FILE" exec -T postgres backups

log "Backup complete!"
