# KAVAN v6.0 — Production Deployment Guide

This document describes how to deploy the KAVAN backend infrastructure in a production environment.

---

## 1. Prerequisites

- Host OS: Ubuntu 22.04 LTS or newer
- Python 3.12 installed
- PostgreSQL 16+ running
- Redis 7+ running
- Nginx reverse proxy

---

## 2. Setting Up the Host Environment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-org/kavan.git /opt/kavan
   cd /opt/kavan
   ```

2. **Set up virtual environment**:
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r backend/requirements.txt
   ```

3. **Configure Environment Variables**:
   Copy `.env.template` to `.env` inside `backend/` and modify values appropriately:
   ```bash
   cp backend/.env.template backend/.env
   nano backend/.env
   ```

---

## 3. Configuration & Databases

1. **Run migrations**:
   ```bash
   python backend/manage.py migrate
   ```

2. **Collect static files**:
   ```bash
   python backend/manage.py collectstatic --no-input
   ```

---

## 4. Setting Up Services (Systemd)

We use systemd to manage the Gunicorn application server and Celery background workers.
Copy systemd configurations from `backend/deployment/systemd/` to `/etc/systemd/system/`:

```bash
sudo cp backend/deployment/systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload
```

Enable and start services:
```bash
sudo systemctl enable kavan-api kavan-celery kavan-beat
sudo systemctl start kavan-api kavan-celery kavan-beat
```

---

## 5. Nginx Configuration

Copy the Nginx configuration template to sites-available:
```bash
sudo cp nginx/kavan.conf /etc/nginx/sites-available/kavan.conf
sudo ln -s /etc/nginx/sites-available/kavan.conf /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```
