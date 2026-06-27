#!/bin/bash
# ============================================================
# KAVAN v6.0 — Database Restore Script
# ============================================================

set -euo pipefail

BACKUP_FILE="${1:-}"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <path_to_backup_file.sql.gz>"
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo "ERROR: Backup file not found: $BACKUP_FILE"
    exit 1
fi

DB_NAME="${DB_NAME:-kavan_db}"
DB_USER="${DB_USER:-kavan_user}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_PASSWORD="${DB_PASSWORD:-kavan_secure_password}"

echo "============================================================"
echo "WARNING: Restoring database '$DB_NAME' from:"
echo "  $BACKUP_FILE"
echo "This will OVERWRITE all existing database records."
echo "============================================================"
read -p "Type 'yes' to confirm: " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Aborted."
    exit 0
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Stopping application services..."
sudo systemctl stop kavan-api kavan-celery kavan-beat || true

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Restoring database..."
gunzip -c "$BACKUP_FILE" | PGPASSWORD="${DB_PASSWORD}" psql \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting application services..."
sudo systemctl start kavan-api kavan-celery kavan-beat || true

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Database restore completed successfully."
