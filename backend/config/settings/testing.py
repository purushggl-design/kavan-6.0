"""
KAVAN v6.0 — Testing Settings
============================================================
Optimized settings for fast test execution:
  - In-memory SQLite DB
  - Eager/synchronous Celery tasks
  - MD5 Password Hasher (much faster than PBKDF2/bcrypt)
  - Muted logging noise
"""

from .base import *  # noqa: F401, F403

# Core
DEBUG = False
TESTING = True

# In-memory Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# In-memory Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "kavan-testing-cache",
    }
}

# Celery: synchronous execution
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Fast password hasher
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Email backend: LocMem for testing checks
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Disable logging noise during test run
logging.disable(logging.CRITICAL)  # Mutes logs globally for speed

# Simplify LOGGING config to prevent file writes during tests
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["null"],
            "level": "CRITICAL",
        },
    },
}
