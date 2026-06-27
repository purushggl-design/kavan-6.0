# ============================================================
# KAVAN v6.0 — Feature Flags Configuration
# ============================================================

from decouple import config

# All flags default to secure/standard settings if not specified.
ENABLE_CACHE = config("ENABLE_CACHE", default=True, cast=bool)
ENABLE_METRICS = config("ENABLE_METRICS", default=True, cast=bool)
ENABLE_CELERY = config("ENABLE_CELERY", default=True, cast=bool)
ENABLE_AUDIT = config("ENABLE_AUDIT", default=True, cast=bool)
ENABLE_SWAGGER = config("ENABLE_SWAGGER", default=True, cast=bool)
ENABLE_DEBUG_TOOLBAR = config("ENABLE_DEBUG_TOOLBAR", default=False, cast=bool)
ENABLE_HEALTH_LOGGING = config("ENABLE_HEALTH_LOGGING", default=True, cast=bool)
ENABLE_RATE_LIMIT = config("ENABLE_RATE_LIMIT", default=False, cast=bool)
ENABLE_CORRELATION_ID = config("ENABLE_CORRELATION_ID", default=True, cast=bool)
