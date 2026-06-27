# KAVAN v6.0

> Enterprise Identity & Access Management Platform — Django REST API

---

## Architecture Progress

| Layer | Status |
|-------|--------|
| Layer 1 — Infrastructure | ✅ Complete |
| Layer 2 — Identity & Access Management | 🔨 In Progress (Module 1 done) |
| Layer 3 — Multi-Tenant Engine | ⏳ Pending |
| Layer 4 — RBAC | ⏳ Pending |
| Layer 5–10 | ⏳ Pending |

---

## Prerequisites

Make sure the following are installed and running on your machine before starting:

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.10+ | Used by the backend |
| PostgreSQL | 16+ | Primary database |
| Redis | 7+ | Cache, broker, blacklist |

---

## Quick Start (Local — No Docker)

All commands below assume you are inside the `backend/` directory.

### Step 1 — Virtual Environment

```powershell
# Create the virtual environment (first time only)
python -m venv venv

# Activate it (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate it (Linux / macOS)
source venv/bin/activate
```

### Step 2 — Install Dependencies

```powershell
# Install all production + dev dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Step 3 — Environment Variables

Copy the template and fill in your local values:

```powershell
# Windows
Copy-Item ..\.env.template ..\.env

# Linux / macOS
cp ../.env.template ../.env
```

Open `.env` (root of the project) and configure:

```env
# Database (local PostgreSQL)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=kavan_db
DB_USER=kavan_user
DB_PASSWORD=kavan_secure_password

# Redis (local)
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# Security
SECRET_KEY=your-secret-key-here
DEBUG=True
DJANGO_SETTINGS_MODULE=config.settings.local
```

### Step 4 — Database Setup

Run this once in PostgreSQL (psql or pgAdmin):

```sql
CREATE DATABASE kavan_db;
CREATE USER kavan_user WITH PASSWORD 'kavan_secure_password';
GRANT ALL PRIVILEGES ON DATABASE kavan_db TO kavan_user;
```

### Step 5 — Apply Migrations

```powershell
python manage.py migrate --settings=config.settings.local
```

### Step 6 — Run the Services

Open **three separate terminals** inside `backend/`, with the venv activated in each.

#### Terminal 1 — Django API Server
```powershell
python manage.py runserver --settings=config.settings.local
```
> API available at: **http://localhost:8000**
> Swagger UI: **http://localhost:8000/api/docs/**
> Health check: **http://localhost:8000/api/health/**

#### Terminal 2 — Celery Worker
```powershell
celery -A config.celery worker --loglevel=info
```

#### Terminal 3 — Celery Beat (Scheduler)
```powershell
celery -A config.celery beat --loglevel=info
```

---

## Verify Everything Is Working

After starting the API server, open a browser or use curl/Postman:

```powershell
# Health check — should return 200 OK
curl http://localhost:8000/api/health/

# API root
curl http://localhost:8000/api/v1/
```

Expected health response:
```json
{
  "success": true,
  "message": "All systems operational.",
  "data": { "status": "healthy" }
}
```

---

## Layer 2 — IAM Tables in Database

After running migrations, these tables will be present:

| Table | Description |
|-------|-------------|
| `iam_users` | Core user model (UUID PK, status enum, MFA flag) |
| `iam_refresh_tokens` | JWT refresh tokens (hashed, revocable) |
| `iam_email_verifications` | Email verification tokens |
| `iam_password_resets` | Password reset tokens |
| `iam_service_accounts` | Machine identity stub (Layer 8) |
| `iam_password_history` | Last N password hashes (no-reuse policy) |
| `iam_user_profiles` | Extended profile, timezone, preferences |
| `iam_sessions` | Active user sessions per device |
| `iam_trusted_devices` | Device fingerprints and trust status |
| `iam_mfa_secrets` | Encrypted TOTP secrets (Fernet AES-256) |
| `iam_backup_codes` | One-time MFA recovery codes (hashed) |
| `iam_audit_events` | Immutable audit log (append-only) |

---

## Project Structure

```
kavan/
├── .env                        # Environment variables (not in git)
├── .env.template               # Template for .env
├── docker-compose.yml          # Docker setup (optional)
├── README.md                   # This file
│
└── backend/
    ├── manage.py
    ├── requirements.txt        # Production dependencies
    ├── requirements-dev.txt    # Dev + test dependencies
    │
    ├── config/                 # Django configuration
    │   ├── settings/
    │   │   ├── base.py         # Shared settings
    │   │   ├── local.py        # Local development
    │   │   └── production.py   # Production
    │   ├── auth_config.py      # Layer 2 security settings (NEW)
    │   ├── urls.py
    │   ├── celery.py
    │   └── api_router.py
    │
    ├── apps/                   # Django applications
    │   ├── authentication/     # Layer 2: Users, JWT, tokens
    │   ├── accounts/           # Layer 2: Password management
    │   ├── profiles/           # Layer 2: User profiles
    │   ├── sessions/           # Layer 2: Session management
    │   ├── devices/            # Layer 2: Device tracking
    │   ├── mfa/                # Layer 2: TOTP / backup codes
    │   ├── audit/              # Layer 2: Audit log
    │   ├── core/               # Layer 1: Core utilities
    │   └── health/             # Layer 1: Health check API
    │
    └── common/                 # Shared utilities
        ├── models/mixins.py    # UUID, Timestamp, SoftDelete
        ├── repositories/       # Base repository pattern
        ├── responses/          # Standard API response
        └── logging/            # Structured JSON logging
```

---

## Running Tests

```powershell
# Run full test suite
pytest --settings=config.settings.local -v

# Run with coverage report
pytest --settings=config.settings.local --cov=apps --cov-report=term-missing
```

---

## Code Quality

```powershell
# Format code
black .
isort .

# Lint
flake8 .
mypy .
```

---

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | *(required)* | Django secret key |
| `DEBUG` | `False` | Enable debug mode |
| `DB_HOST` | `localhost` | PostgreSQL host |
| `DB_PORT` | `5432` | PostgreSQL port |
| `DB_NAME` | `kavan_db` | Database name |
| `DB_USER` | `kavan_user` | Database user |
| `DB_PASSWORD` | *(required)* | Database password |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection URL |
| `JWT_ACCESS_TOKEN_TTL` | `900` | Access token lifetime (seconds) |
| `JWT_REFRESH_TOKEN_TTL` | `2592000` | Refresh token lifetime (seconds) |
| `SESSION_MAX_CONCURRENT` | `5` | Max concurrent sessions per user |
| `PASSWORD_MIN_LENGTH` | `12` | Minimum password length |
| `ENABLE_RATE_LIMIT` | `False` | Enable API rate limiting |
| `ENABLE_SWAGGER` | `True` | Enable Swagger UI |
| `LOG_LEVEL` | `INFO` | Logging level |