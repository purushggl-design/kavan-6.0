# KAVAN v6.0 — Environment Variables Reference

All runtime configurations are loaded from environment variables using `python-decouple`.

---

## 1. Application Identity

- `APP_NAME`: Name of the application (default: `KAVAN`).
- `APP_VERSION`: Current semantic version of the application (default: `6.0.0`).
- `APP_ENV`: Deployment stage environment: `local`, `development`, `testing`, `staging`, `production`.

---

## 2. Security

- `SECRET_KEY`: Long, complex secret key for signing sessions and CSRF tokens. Must be unique per deployment.
- `DEBUG`: Boolean flag (`True` / `False`) mapping if Django is in debug mode. Must be `False` in production.
- `ALLOWED_HOSTS`: Comma-separated list of domain names/IPs the application accepts.
- `CORS_ALLOWED_ORIGINS`: Comma-separated list of origins permitted to make cross-domain HTTP requests.
- `CORS_ALLOW_ALL_ORIGINS`: Boolean flag enabling public CORS endpoints (default: `False`).

---

## 3. Database (PostgreSQL)

- `DB_ENGINE`: Django DB engine class (`django.db.backends.postgresql`).
- `DB_NAME`: Database name.
- `DB_USER`: Database username.
- `DB_PASSWORD`: Password for the DB user.
- `DB_HOST`: Host address of the database server.
- `DB_PORT`: Port of the database server (default: `5432`).

---

## 4. Cache & Broker (Redis)

- `REDIS_URL`: Connection string for Redis cache (e.g. `redis://localhost:6379/0`).
- `CELERY_BROKER_URL`: Connection string for Celery broker (e.g. `redis://localhost:6379/0`).
- `CELERY_RESULT_BACKEND`: Connection string for Celery backend (e.g. `redis://localhost:6379/1`).

---

## 5. Feature Flags

- `ENABLE_CACHE`: Boolean toggle for using cache.
- `ENABLE_METRICS`: Boolean toggle to collect Prometheus/app metrics.
- `ENABLE_CELERY`: Boolean toggle for background tasks.
- `ENABLE_AUDIT`: Boolean toggle for audit trail middleware logging.
- `ENABLE_SWAGGER`: Boolean toggle for API document generation.
- `ENABLE_RATE_LIMIT`: Boolean toggle for throttling policies.
- `ENABLE_CORRELATION_ID`: Boolean toggle for Correlation ID middleware propagation.
