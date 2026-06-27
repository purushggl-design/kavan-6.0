# KAVAN v6.0 — Setup Guide

## Prerequisites

- Python 3.12+
- PostgreSQL 16+
- Redis 7+
- Docker + Docker Compose (optional)

---

## Setup Steps

### 1. Virtual Environment
```bash
cd backend
python -m venv venv
source venv/bin/activate          # Linux/Mac
# or: venv\Scripts\activate       # Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements-dev.txt
```

### 3. Environment Variables
```bash
cp .env.template .env
# Edit backend/.env:
#   DB_HOST=localhost
#   REDIS_URL=redis://localhost:6379/0
#   DEBUG=True
```

### 4. Database Setup
```bash
# Create PostgreSQL database
createdb kavan_db
createuser kavan_user
psql -c "GRANT ALL PRIVILEGES ON DATABASE kavan_db TO kavan_user;"

# Run migrations
python manage.py migrate
```

### 5. Start Services
```bash
# Terminal 1: Django dev server
python manage.py runserver

# Terminal 2: Celery worker
celery -A config.celery worker --loglevel=info

# Terminal 3: Celery beat (optional)
celery -A config.celery beat --loglevel=info
```

### 6. Verify
```bash
curl http://localhost:8000/health/
curl http://localhost:8000/health/live/
curl http://localhost:8000/health/ready/
```

---

## Running Tests

```bash
cd backend
pytest tests/ -v --tb=short
pytest tests/unit/           # Unit tests only
pytest tests/integration/    # Integration tests
pytest tests/security/       # Security tests
pytest --cov=. --cov-report=html  # With coverage
```

---

## Development Commands

```bash
# Check code style
black --check .
isort --check-only .
flake8 .

# Format code
black .
isort .

# Security scan
bandit -r . -x tests/
safety check -r requirements.txt

# Create migration
python manage.py makemigrations

# Django shell
python manage.py shell_plus  # (requires django-extensions)
```
