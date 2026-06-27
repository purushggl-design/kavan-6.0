# KAVAN v6.0 — Troubleshooting Guide

## Common Issues

---

### ❌ `django.db.utils.OperationalError: could not connect to server`

**Cause:** Django cannot reach PostgreSQL.

**Fix:**
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Check DB_HOST in .env
# For docker-compose: DB_HOST=db
# For local:         DB_HOST=localhost

# Test connection manually
psql -h localhost -U kavan_user -d kavan_db
```

---

### ❌ `redis.exceptions.ConnectionError`

**Cause:** Redis is not reachable.

**Fix:**
```bash
# Check Redis is running
sudo systemctl status redis
redis-cli ping  # Should return PONG

# Verify REDIS_URL in .env
# docker-compose: REDIS_URL=redis://redis:6379/0
# local:         REDIS_URL=redis://localhost:6379/0
```

---

### ❌ `ModuleNotFoundError: No module named 'config'`

**Cause:** Python path doesn't include the `backend/` directory.

**Fix:**
```bash
# Always run from backend/ directory
cd backend
python manage.py runserver

# Or set PYTHONPATH
export PYTHONPATH=/opt/kavan/backend:$PYTHONPATH
```

---

### ❌ `django.core.exceptions.ImproperlyConfigured: SECRET_KEY`

**Cause:** `.env` file not present or SECRET_KEY not set.

**Fix:**
```bash
cp .env.template .env
# Edit SECRET_KEY= with a 50+ character random string
python -c "from django.utils.crypto import get_random_string; print(get_random_string(50))"
```

---

### ❌ Health check returns `{"status": "not_ready"}`

**Cause:** Database or Redis not reachable during startup.

**Fix:**
1. Check `GET /health/db/` and `GET /health/redis/` individually
2. Verify services are running: `docker-compose ps`
3. Check connection settings in `.env`

---

### ❌ Celery tasks not executing

**Cause:** Worker not running or broker connection failed.

**Fix:**
```bash
# Start a worker manually
celery -A config.celery worker --loglevel=debug

# Check broker URL
celery -A config.celery inspect ping
```

---

### ❌ `PermissionDenied` on staticfiles

**Cause:** Static files directory not writable by kavan user.

**Fix:**
```bash
sudo chown -R kavan:kavan /opt/kavan/backend/staticfiles
chmod 755 /opt/kavan/backend/staticfiles
```

---

## Log Files

| Log | Location | Command |
|-----|----------|---------|
| API logs | `/var/log/kavan/app.log` | `tail -f /var/log/kavan/app.log` |
| Security logs | `/var/log/kavan/security.log` | `tail -f /var/log/kavan/security.log` |
| Celery | `/var/log/kavan/celery-1.log` | `tail -f /var/log/kavan/celery-1.log` |
| Systemd | journald | `journalctl -u kavan-api -f` |

---

## Useful Commands

```bash
# Check all service statuses
sudo systemctl status kavan-api kavan-celery kavan-beat

# Restart all services
sudo systemctl restart kavan-api kavan-celery kavan-beat

# View recent logs
journalctl -u kavan-api -n 100 --no-pager

# Run Django shell
cd /opt/kavan/backend
source ../venv/bin/activate
python manage.py shell

# Check pending migrations
python manage.py showmigrations

# Check Celery worker status
celery -A config.celery inspect active
celery -A config.celery inspect stats
```
