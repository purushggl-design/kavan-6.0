# KAVAN v6.0 — Documentation

## Overview

KAVAN v6.0 is an enterprise-grade, multi-tenant product launch and management platform built on Django REST Framework. This repository contains **Layer 1: Infrastructure** — the complete foundation upon which all business logic layers are built.

---

## Documentation

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture and design decisions |
| [SETUP.md](SETUP.md) | Local development setup guide |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Production deployment guide |
| [API.md](API.md) | API reference and response formats |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Common issues and solutions |

---

## Quick Start

For detailed setup instructions, please refer to the [Setup Guide](SETUP.md).

```bash
# 1. Clone the repository
git clone https://github.com/yourorg/kavan.git
cd kavan

# 2. Follow setup instructions in docs/SETUP.md to configure local Python environment, DB, and Redis.
```

---

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Backend Framework | Django | 5.0+ |
| API Framework | Django REST Framework | 3.15+ |
| Database | PostgreSQL | 16+ |
| Cache / Broker | Redis | 7+ |
| Task Queue | Celery | 5.4+ |
| Application Server | Gunicorn | 22+ |
| Reverse Proxy | Nginx | 1.24+ |
| Python | CPython | 3.12+ |
| OS (Production) | Ubuntu | 24.04 LTS |

---

## Layer Architecture

```
Layer 1: Infrastructure (THIS LAYER)
  ├── Configuration, Middleware, Exceptions, Logging
  └── Health checks, Monitoring, Deployment

Layer 2: Authentication (NEXT)
  └── JWT auth, User model, Sessions

Layer 3: Multi-Tenancy
  └── Tenant model, tenant-scoped data

Layer 4: RBAC
  └── Roles, Permissions, Policy enforcement

Layer 5+: Business Logic
  └── Products, Launches, Reporting, etc.
```

---

## License

Copyright © 2026 KAVAN Technologies. All rights reserved.
