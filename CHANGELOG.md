# Changelog

All notable changes to the KAVAN project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [6.0.0] - 2026-06-26

### Added
- Enterprise-ready infrastructure foundation using Django, DRF, and PostgreSQL.
- Structured JSON logging handler mapping requests, Celery, and DB logs.
- Thread-local RequestContext propagation of Request-ID, Correlation-ID, client IP, and tenant.
- System metrics collectors utilizing `psutil` exposing CPU, memory, and disk info.
- Fully integrated drf-spectacular settings for OpenAPI schema output and Swagger endpoints.
- Lightweight IoC Container (`ServiceContainer`) and providers for dynamic repository resolution.
- Database and media backup and restore shell scripts.
- Security hardening middleware enforcing strict CSP policies and payload limitations.
- Static analysis checks (Ruff, Black, isort, mypy) and GitHub Actions workflows.
