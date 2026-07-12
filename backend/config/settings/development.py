"""
KAVAN v6.0 — Development Settings
============================================================
Extends base settings with developer-friendly overrides:
  - DEBUG enabled
  - Console logging (verbose)
  - Relaxed CORS
  - Django Debug Toolbar
  - SQLite fallback when no PostgreSQL available
"""

from .base import *  # noqa: F401, F403

# ============================================================
# CORE OVERRIDES
# ============================================================

DEBUG = True

ALLOWED_HOSTS = ["*"]

# ============================================================
# DEBUG TOOLBAR (optional — uncomment if using)
# ============================================================

# INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405
# MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405
# INTERNAL_IPS = ["127.0.0.1", "localhost"]

# ============================================================
# LOGGING — OVERRIDE: Verbose console output
# ============================================================

LOGGING["handlers"]["console"]["formatter"] = "verbose"  # noqa: F405
LOGGING["loggers"][""]["level"] = "DEBUG"  # noqa: F405
LOGGING["loggers"]["kavan"]["level"] = "DEBUG"  # noqa: F405
LOGGING["loggers"]["django"]["level"] = "INFO"  # noqa: F405
LOGGING["loggers"]["django.db.backends"]["level"] = "DEBUG"  # noqa: F405

# ============================================================
# CORS — Relaxed for development
# ============================================================

CORS_ALLOW_ALL_ORIGINS = True  # noqa: F405
CORS_ALLOW_CREDENTIALS = True  # noqa: F405

# ============================================================
# EMAIL — Console backend (no SMTP needed)
# ============================================================

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"  # noqa: F405

# ============================================================
# CACHES — Local memory for development (no Redis needed)
# Uncomment the Redis cache to test Redis locally.
# ============================================================

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "kavan-dev",
    }
}

# ============================================================
# CELERY — Eager execution for local debugging
# Tasks run synchronously in dev (no broker/Redis needed).
# Ensure no broker is required in dev if not available
CELERY_BROKER_URL = "memory://"
CELERY_RESULT_BACKEND = "cache+memory://"
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# ============================================================
# DRF — Show browsable API in development
# ============================================================

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [  # noqa: F405
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
]

# ============================================================
# SECURITY — Relaxed for development
# ============================================================

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
