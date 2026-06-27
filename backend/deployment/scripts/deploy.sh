#!/bin/bash
# ============================================================
# KAVAN v6.0 — Deployment Script
# Usage: sudo -u kavan bash deploy.sh
# ============================================================

set -euo pipefail

# Configuration
APP_DIR="/opt/kavan"
BACKEND_DIR="$APP_DIR/backend"
VENV_DIR="$APP_DIR/venv"
GIT_REPO="https://github.com/yourorg/kavan.git"
GIT_BRANCH="${DEPLOY_BRANCH:-main}"
LOG_FILE="/var/log/kavan/deploy.log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() { echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}" | tee -a "$LOG_FILE"; }
warn() { echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}" | tee -a "$LOG_FILE"; }
error() { echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}" | tee -a "$LOG_FILE"; exit 1; }

log "======================================================"
log "KAVAN v6.0 Deployment Starting"
log "Branch: $GIT_BRANCH"
log "======================================================"

# ----------------------------------------------------------
# Pre-deployment health check
# ----------------------------------------------------------
log "Running pre-deployment health check..."
curl -sf http://localhost:8000/health/ready/ || warn "Pre-deployment health check failed (continuing)"

# ----------------------------------------------------------
# 1. Pull latest code
# ----------------------------------------------------------
log "Pulling latest code from $GIT_BRANCH..."
cd "$APP_DIR"
git fetch origin
git checkout "$GIT_BRANCH"
git pull origin "$GIT_BRANCH"

# ----------------------------------------------------------
# 2. Activate virtual environment
# ----------------------------------------------------------
log "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# ----------------------------------------------------------
# 3. Install/update dependencies
# ----------------------------------------------------------
log "Installing Python dependencies..."
cd "$BACKEND_DIR"
pip install -r requirements.txt --quiet

# ----------------------------------------------------------
# 4. Run database migrations
# ----------------------------------------------------------
log "Running database migrations..."
python manage.py migrate --noinput

# ----------------------------------------------------------
# 5. Collect static files
# ----------------------------------------------------------
log "Collecting static files..."
python manage.py collectstatic --noinput --clear

# ----------------------------------------------------------
# 6. Restart services
# ----------------------------------------------------------
log "Restarting KAVAN services..."
sudo systemctl daemon-reload
sudo systemctl restart kavan-api
sudo systemctl restart kavan-celery
sudo systemctl restart kavan-beat

# Wait for services to start
sleep 5

# ----------------------------------------------------------
# 7. Post-deployment health check
# ----------------------------------------------------------
log "Running post-deployment health check..."
HEALTH_RESPONSE=$(curl -sf http://localhost:8000/health/ready/ || echo "FAILED")

if echo "$HEALTH_RESPONSE" | grep -q '"status":"ready"'; then
    log "✅ Post-deployment health check PASSED"
else
    error "❌ Post-deployment health check FAILED. Check logs: journalctl -u kavan-api -n 50"
fi

log "======================================================"
log "✅ Deployment completed successfully"
log "======================================================"
