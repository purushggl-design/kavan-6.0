#!/bin/bash
# ============================================================
# KAVAN v6.0 — Media Files Restore Script
# ============================================================

set -euo pipefail

BACKUP_FILE="${1:-}"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <path_to_backup_file.tar.gz>"
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo "ERROR: Backup file not found: $BACKUP_FILE"
    exit 1
fi

MEDIA_DIR="${MEDIA_DIR:-/opt/kavan/backend/media}"

echo "============================================================"
echo "WARNING: Restoring media files to '$MEDIA_DIR' from:"
echo "  $BACKUP_FILE"
echo "Existing files in the destination may be overwritten."
echo "============================================================"
read -p "Type 'yes' to confirm: " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Aborted."
    exit 0
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Stopping application services..."
sudo systemctl stop kavan-api kavan-celery kavan-beat || true

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Extracting files to media directory..."
mkdir -p "$MEDIA_DIR"
tar -xzf "$BACKUP_FILE" -C "$(dirname "$MEDIA_DIR")"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting application services..."
sudo systemctl start kavan-api kavan-celery kavan-beat || true

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Media restore completed successfully."
