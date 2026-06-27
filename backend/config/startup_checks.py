"""
KAVAN v6.0 — Configuration Validation on Startup
============================================================
Checks environment variables, database, Redis connectivity, and directories on boot.
"""

import os
import logging
from django.conf import settings
from django.db import connections
from django.core.cache import cache

logger = logging.getLogger("kavan")

def validate_configuration() -> None:
    """
    Verifies that the current environment is configured correctly.
    Logs warnings in development and raises ValueError on failures in production.
    """
    # Skip checks if running test suite or during specific CLI commands (like migrations)
    import sys
    if "test" in sys.argv or "pytest" in sys.modules or "makemigrations" in sys.argv:
        return

    logger.info("Running startup configuration checks...")
    
    errors = []
    warnings = []
    is_prod = not getattr(settings, "DEBUG", False)

    # 1. SECRET_KEY validation
    secret_key = getattr(settings, "SECRET_KEY", "")
    if not secret_key or "change-me" in secret_key or len(secret_key) < 32:
        msg = f"SECRET_KEY is insecure or too short ({len(secret_key)} chars)."
        if is_prod:
            errors.append(msg)
        else:
            warnings.append(msg)

    # 2. ALLOWED_HOSTS check
    allowed_hosts = getattr(settings, "ALLOWED_HOSTS", [])
    if is_prod and (not allowed_hosts or "*" in allowed_hosts):
        errors.append("ALLOWED_HOSTS must be strictly configured in production. Cannot be empty or contain '*'.")

    # 3. Log Directory check
    log_dir = getattr(settings, "LOG_DIR", None)
    if log_dir:
        try:
            os.makedirs(log_dir, exist_ok=True)
            test_file = os.path.join(log_dir, ".write_test")
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
        except Exception as e:
            errors.append(f"Logs directory '{log_dir}' is not writable: {e}")

    # 4. Database Connectivity check
    try:
        db_conn = connections["default"]
        db_conn.ensure_connection()
    except Exception as e:
        msg = f"Database connection test failed: {e}."
        if is_prod:
            errors.append(msg)
        else:
            warnings.append(msg)

    # 5. Redis/Cache Connectivity check
    try:
        from config.feature_flags import ENABLE_CACHE
        if ENABLE_CACHE:
            cache.set("kavan_startup_check", "ok", timeout=5)
            val = cache.get("kavan_startup_check")
            if val != "ok":
                warnings.append("Redis Cache is connected but failing write/read integrity checks.")
    except Exception as e:
        msg = f"Redis Cache connection test failed: {e}."
        if is_prod:
            errors.append(msg)
        else:
            warnings.append(msg)

    # Log warnings
    for warn in warnings:
        logger.warning(f"[STARTUP WARNING] {warn}")

    # Raise or log errors
    if errors:
        for err in errors:
            logger.error(f"[STARTUP ERROR] {err}")
        if is_prod:
            raise ValueError(f"Production configuration validation failed: {'; '.join(errors)}")
        else:
            logger.warning("Startup check failed, but proceeding because DEBUG=True.")
    else:
        logger.info("Startup configuration checks passed successfully.")
