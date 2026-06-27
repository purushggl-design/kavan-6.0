#!/bin/bash
# ============================================================
# KAVAN v6.0 — Database Restore Script
# Usage: bash restore.sh /var/backups/kavan/db/kavan_20260626_020000.sql.gz
# ============================================================

set -euo pipefail

BACKUP_FILE="${1:-}"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file.sql.gz>"
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

echo "WARNING: This will restore $DB_NAME from $BACKUP_FILE"
echo "All existing data will be OVERWRITTEN."
read -p "Type 'yes' to confirm: " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Restore cancelled."
    exit 0
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Stopping KAVAN services..."
sudo systemctl stop kavan-api kavan-celery kavan-beat || true

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Restoring database from $BACKUP_FILE..."
gunzip -c "$BACKUP_FILE" | PGPASSWORD="${DB_PASSWORD}" psql \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Restore complete. Starting KAVAN services..."
sudo systemctl start kavan-api kavan-celery kavan-beat

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Restore completed successfully."
