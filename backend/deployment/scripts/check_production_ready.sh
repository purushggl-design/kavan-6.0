#!/bin/bash
# ============================================================
# KAVAN v6.0 — Production Readiness Check
# ============================================================

set -euo pipefail

# Ensure we use production settings for the verification
export DJANGO_SETTINGS_MODULE="config.settings.production"

echo "============================================================"
echo "🛡️  Running KAVAN v6.0 Production Readiness Check..."
echo "============================================================"

# Navigate to backend directory if not already there
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/../.."

python - <<EOF
import os
import sys
import django

# Bootstrap django settings
try:
    django.setup()
except Exception as e:
    print(f"[CRITICAL FAIL] Django bootstrap failed: {e}")
    sys.exit(1)

from django.conf import settings
from django.db import connections
from django.core.cache import cache

failures = 0
warnings = 0

def report(passed, text, critical=True):
    global failures, warnings
    if passed:
        print(f"  [PASS]  ✅ {text}")
    else:
        if critical:
            print(f"  [FAIL]  ❌ {text}")
            failures += 1
        else:
            print(f"  [WARN]  ⚠️  {text}")
            warnings += 1

print("\n--- 1. Django Basic Settings ---")
report(not settings.DEBUG, "DEBUG is set to False (production mode)")
report("change-me" not in settings.SECRET_KEY, "SECRET_KEY is modified from template")
report(len(settings.SECRET_KEY) >= 40, f"SECRET_KEY length is secure ({len(settings.SECRET_KEY)} chars)")
report("*" not in settings.ALLOWED_HOSTS, "ALLOWED_HOSTS does not contain '*' wildcard")

print("\n--- 2. SSL & Cookies Protection ---")
report(settings.SECURE_SSL_REDIRECT, "SECURE_SSL_REDIRECT is enabled")
report(settings.SESSION_COOKIE_SECURE, "SESSION_COOKIE_SECURE is enabled")
report(settings.CSRF_COOKIE_SECURE, "CSRF_COOKIE_SECURE is enabled")
report(settings.SESSION_COOKIE_HTTPONLY, "SESSION_COOKIE_HTTPONLY is enabled")
report(settings.CSRF_COOKIE_HTTPONLY, "CSRF_COOKIE_HTTPONLY is enabled")

print("\n--- 3. Static Files ---")
report(settings.STATIC_ROOT is not None, "STATIC_ROOT directory configured")
report("whitenoise" in settings.STATICFILES_STORAGE.lower(), f"WhiteNoise compress storage is active: {settings.STATICFILES_STORAGE}")

print("\n--- 4. Active Connections ---")
# DB Check
try:
    connections['default'].ensure_connection()
    report(True, "PostgreSQL Database connection established")
except Exception as e:
    report(False, f"PostgreSQL Database unreachable: {e}")

# Redis check
try:
    cache.set("kavan_prod_test", "verified", timeout=5)
    val = cache.get("kavan_prod_test")
    report(val == "verified", "Redis Cache connectivity verified successfully")
except Exception as e:
    report(False, f"Redis Cache unreachable: {e}")

print("\n--- 5. Log Directories ---")
log_dir = getattr(settings, "LOG_DIR", None)
if log_dir and os.path.exists(log_dir):
    report(os.access(log_dir, os.W_OK), f"Logs directory is writable: {log_dir}")
else:
    report(False, f"Logs directory does not exist or is not specified: {log_dir}")

print("\n============================================================")
if failures > 0:
    print(f"❌ PRODUCTION READINESS STATUS: FAILED ({failures} critical errors, {warnings} warnings)")
    sys.exit(1)
else:
    print(f"✅ PRODUCTION READINESS STATUS: PASSED ({warnings} warnings)")
    sys.exit(0)
EOF
