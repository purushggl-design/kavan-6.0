#!/bin/bash
# ============================================================
# KAVAN v6.0 — Media Files Backup Script
# ============================================================

set -euo pipefail

MEDIA_DIR="${MEDIA_DIR:-/opt/kavan/backend/media}"
BACKUP_DIR="${BACKUP_DIR:-/var/backups/kavan/media}"
RETENTION_DAYS=14
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
BACKUP_FILE="$BACKUP_DIR/kavan_media_${TIMESTAMP}.tar.gz"

mkdir -p "$BACKUP_DIR"

if [ ! -d "$MEDIA_DIR" ]; then
    echo "ERROR: Media directory does not exist: $MEDIA_DIR"
    exit 1
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting media files backup..."

# Use tar to archive the media directory
tar -czf "$BACKUP_FILE" -C "$(dirname "$MEDIA_DIR")" "$(basename "$MEDIA_DIR")"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Media backup saved: $BACKUP_FILE ($(du -sh "$BACKUP_FILE" | cut -f1))"

# Retention cleaning
find "$BACKUP_DIR" -name "kavan_media_*.tar.gz" -mtime +$RETENTION_DAYS -delete
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Cleaned media backups older than $RETENTION_DAYS days"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Media backup completed."
