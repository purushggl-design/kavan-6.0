# KAVAN v6.0 Architecture Report

## Core Principles
1. **Clean Architecture**: Strong boundary enforcement.
   - `Views` handle HTTP parsing.
   - `Services` handle Business Logic.
   - `Repositories` handle Database I/O.
   - `Models` represent pure schema structure.
2. **Multi-Tenancy**: Data isolated at the application level via `TenantContextMiddleware` and `TenantScopedManager`.
3. **Decoupled Engine**: Layer 6 Deployments acts as an asynchronous engine downstream of Layer 5 Marketplace Subscriptions.

## Component Stack
- **API Framework**: Django Rest Framework (DRF)
- **Database**: PostgreSQL (UUID Primary Keys)
- **Caching & RBAC**: Redis (In-memory permission lookups)
- **Background Jobs**: Celery (Publishing, Syncing, Deployment Orchestration)
- **Documentation**: drf-spectacular (Swagger/OpenAPI)
