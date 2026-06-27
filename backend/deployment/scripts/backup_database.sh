#!/bin/bash
# ============================================================
# KAVAN v6.0 — Database Backup Script (pg_dump with gzip)
# ============================================================

set -euo pipefail

DB_NAME="${DB_NAME:-kavan_db}"
DB_USER="${DB_USER:-kavan_user}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_PASSWORD="${DB_PASSWORD:-kavan_secure_password}"
BACKUP_DIR="${BACKUP_DIR:-/var/backups/kavan/db}"
RETENTION_DAYS=30
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
BACKUP_FILE="$BACKUP_DIR/kavan_db_${TIMESTAMP}.sql.gz"

mkdir -p "$BACKUP_DIR"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting database backup for $DB_NAME..."

# Dump and compress
PGPASSWORD="${DB_PASSWORD}" pg_dump \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    --no-owner \
    --no-privileges \
    | gzip > "$BACKUP_FILE"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Backup saved: $BACKUP_FILE ($(du -sh "$BACKUP_FILE" | cut -f1))"

# Retention cleaning
find "$BACKUP_DIR" -name "kavan_db_*.sql.gz" -mtime +$RETENTION_DAYS -delete
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Cleaned backups older than $RETENTION_DAYS days"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Database backup completed."
