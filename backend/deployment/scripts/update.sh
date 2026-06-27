#!/bin/bash
# ============================================================
# KAVAN v6.0 — Zero-Downtime Update Script
# Performs hot-reload of Gunicorn workers without dropping connections.
# Usage: bash update.sh
# ============================================================

set -euo pipefail

APP_DIR="/opt/kavan"
BACKEND_DIR="$APP_DIR/backend"
VENV_DIR="$APP_DIR/venv"
GIT_BRANCH="${DEPLOY_BRANCH:-main}"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"; }

log "Starting zero-downtime update..."

# 1. Pull code
cd "$APP_DIR"
git pull origin "$GIT_BRANCH"

# 2. Install dependencies (if changed)
source "$VENV_DIR/bin/activate"
cd "$BACKEND_DIR"
pip install -r requirements.txt --quiet

# 3. Run migrations
python manage.py migrate --noinput

# 4. Collect static files
python manage.py collectstatic --noinput --clear

# 5. Hot-reload Gunicorn (sends HUP signal — no downtime)
log "Sending HUP signal to Gunicorn for zero-downtime reload..."
sudo systemctl reload kavan-api

# 6. Restart Celery (brief interruption — tasks re-queued)
sudo systemctl restart kavan-celery
sudo systemctl restart kavan-beat

sleep 3

# 7. Verify
HEALTH=$(curl -sf http://localhost:8000/health/ready/ | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status','unknown'))" 2>/dev/null || echo "unknown")
if [ "$HEALTH" = "ready" ]; then
    log "✅ Update complete — API is ready."
else
    log "⚠️  Update complete but health check returned: $HEALTH"
fi
