"""
KAVAN v6.0 — Production Settings
============================================================
Extends base settings with hardened production overrides:
  - DEBUG disabled
  - Strict security headers (HSTS, CSP, etc.)
  - Secure cookies
  - Production logging (JSON only — no console)
  - WhiteNoise for static file serving
  - Restricted CORS
"""

from decouple import Csv, config

from .base import *  # noqa: F401, F403

# ============================================================
# CORE OVERRIDES
# ============================================================

DEBUG = False

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="yourdomain.com",
    cast=Csv(),
)

# ============================================================
# SECURITY — HSTS + Secure cookies
# ============================================================

SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# HSTS — 1 year
SECURE_HSTS_SECONDS = config("SECURE_HSTS_SECONDS", default=31536000, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True, cast=bool
)
SECURE_HSTS_PRELOAD = config("SECURE_HSTS_PRELOAD", default=True, cast=bool)

# Cookie security
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Strict"
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "Strict"

# Browser security
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

# ============================================================
# CORS — Restricted
# ============================================================

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="https://yourdomain.com",
    cast=Csv(),
)
CORS_ALLOW_CREDENTIALS = True

# ============================================================
# STATIC FILES — WhiteNoise compression
# ============================================================

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ============================================================
# DRF — JSON only in production
# ============================================================

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [  # noqa: F405
    "rest_framework.renderers.JSONRenderer",
]

# ============================================================
# EMAIL — SMTP
# ============================================================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# ============================================================
# LOGGING — JSON only, no console
# ============================================================

LOGGING["loggers"][""]["handlers"] = ["json_file"]  # noqa: F405
LOGGING["loggers"]["kavan"]["handlers"] = ["json_file"]  # noqa: F405
LOGGING["loggers"]["kavan"]["level"] = "INFO"  # noqa: F405
LOGGING["loggers"]["django"]["handlers"] = ["error_file"]  # noqa: F405
LOGGING["loggers"]["django.request"]["handlers"] = ["error_file"]  # noqa: F405
LOGGING["loggers"]["celery"]["handlers"] = ["json_file"]  # noqa: F405

# ============================================================
# CACHES — Production Redis (pool sizing)
# ============================================================

CACHES["default"]["OPTIONS"]["CONNECTION_POOL_KWARGS"] = {  # noqa: F405
    "max_connections": 100
}

# ============================================================
# DATABASE — Production tuning
# ============================================================

DATABASES["default"]["CONN_MAX_AGE"] = 600  # noqa: F405 — 10 min persistent connections
DATABASES["default"]["OPTIONS"] = {  # noqa: F405
    "connect_timeout": 10,
    "options": "-c statement_timeout=30000",  # 30s statement timeout
}
