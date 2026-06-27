"""
KAVAN v6.0 — Staging Settings
============================================================
Extends base settings. Very close to production settings but with:
  - Relaxed SSL redirects (optional / depending on config)
  - Verbose JSON logging (level INFO/DEBUG)
  - Sentry/APM placeholder setup
"""

from decouple import Csv, config

from .base import *  # noqa: F401, F403

# Core
DEBUG = False

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="staging.yourdomain.com",
    cast=Csv(),
)

# Security (Staging can be slightly relaxed for SSL offloading testing)
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=False, cast=bool)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# HSTS - short duration for staging testing
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False

# Cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# CORS
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="https://staging.yourdomain.com",
    cast=Csv(),
)
CORS_ALLOW_CREDENTIALS = True

# Static files whitenoise
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# REST framework
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [  # noqa: F405
    "rest_framework.renderers.JSONRenderer",
]

# Sentry integration placeholder
# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration
# sentry_sdk.init(
#     dsn=config("SENTRY_DSN", default=""),
#     integrations=[DjangoIntegration()],
#     traces_sample_rate=1.0,
#     send_default_pii=True,
# )

# Logging: verbose JSON logging
LOGGING["loggers"][""]["level"] = "INFO"  # noqa: F405
LOGGING["loggers"]["kavan"]["level"] = "DEBUG"  # noqa: F405
LOGGING["loggers"]["django"]["level"] = "INFO"  # noqa: F405
