# KAVAN v6.0 — Project Overview & Architecture Idea

KAVAN v6.0 is an enterprise-grade, multi-tenant product launch and management platform. It is engineered using a decoupled Clean Architecture pattern to provide a robust, scalable, and highly observable foundation for SaaS applications.

---

## 1. Core Vision & Concept

The ultimate goal of KAVAN is to serve as a high-performance orchestrator for managing product lifecycles, rollout calendars, collaborative launches, and cross-functional launch tasks across different enterprise organizations (tenants).

Rather than writing business logic directly in standard, monolithic Django views, KAVAN is built in **strictly decoupled layers** to ensure that components can be tested in isolation, databases or external service dependencies can be swapped easily, and multiple teams can work on different layers without conflict.

---

## 2. Layered Architecture Roadmap

KAVAN is designed as a progressive 5-layer platform. The current repository contains the complete foundation of **Layer 1: Infrastructure**.

```
Layer 5+: Business Logic Layer  ◄ (Product catalogs, launch rollouts, analytics)
       ▼
Layer 4: Advanced RBAC          ◄ (Roles, granular policies, permission scopes)
       ▼
Layer 3: Multi-Tenancy          ◄ (Tenant isolation, tenant-scoped database filters)
       ▼
Layer 2: Authentication         ◄ (JWT Authentication, custom User models, sessions)
       ▼
Layer 1: Infrastructure (CURRENT)◄ (Clean Architecture boilerplate, health probes, logging)
```

---

## 3. The Current Implementation (Layer 1: Infrastructure)

The base layer sets up a rock-solid infrastructure stack, making the application production-ready from day one:

### A. Clean Architecture & Dependency Injection (IoC)
* **Decoupling**: Views (Controllers) never call database models or database-querying code directly. Instead, they depend on abstract **Services**.
* **Repository Pattern**: Data querying and persistence are handled by **Repositories** (`common/repositories/`) which abstract the Django ORM.
* **IoC Service Container**: Dependencies are registered and dynamically resolved using a custom Service Container and Providers (`common/container/` and `common/providers/`). This allows mock objects to be easily injected for testing.

### B. Standardized API Envelope
All API endpoints return a consistent JSON envelope to make client integration seamless:
* **Success Envelope**: Contains status flags, a message, execution metadata, and `data`.
* **Error Envelope**: Provides structured error objects containing specific fields, error codes, and human-readable messages.
* **Pagination Envelope**: Integrates pagination details (current page, total pages, next/previous URLs) into the standard response metadata.

### C. Advanced Observability & Monitoring
* **Request Correlation**: The middleware assigns a unique `X-Request-ID` and `X-Correlation-ID` to every HTTP request, allowing requests to be tracked across microservices and log outputs.
* **Structured JSON Logging**: Custom JSON log formatters serialize system logs with request context, making them easy to index in modern log systems (Elasticsearch, Loki, etc.).
* **Kubernetes-Ready Health Checks**:
  * `/health/`: Detailed system metrics (database connection latency, Redis cache speed, Celery worker capacity).
  * `/health/live/`: Fast check to confirm the server process is alive.
  * `/health/ready/`: Checks connection to dependencies (Postgres, Redis) to verify the pod is ready to accept traffic.

---

## 4. Technology Stack

* **Language**: Python 3.12 (CPython runtime)
* **Framework**: Django 5.0+ & Django REST Framework (DRF) 3.15+
* **Database**: PostgreSQL 16 (for robust transactional and relational data storage)
* **Cache & Message Broker**: Redis 7 (for session caching, rate-limiting, and background tasks)
* **Task Queues**: Celery 5.4 (for asynchronous tasks and scheduled cron jobs via `django-celery-beat`)

---

## 5. Upcoming Architecture Layers

Once Layer 1 is set up, the next phases of development will introduce:

1. **Layer 2 (Authentication)**: 
   * Custom user model with secure password hashing.
   * Stateless JWT (JSON Web Token) authentication with sliding expiration.
   * API security hardening (rate-limiting, CORS control).
2. **Layer 3 (Multi-Tenancy)**:
   * Logical data isolation allowing multiple organizations (tenants) to use the same database while ensuring data cannot leak between them.
   * Middleware to resolve tenants from subdomains or headers.
3. **Layer 4 (RBAC)**:
   * Standardized access control (e.g., Owner, Admin, Editor, Viewer).
   * Feature-based or object-level permissions (e.g., verifying if a user has permission to modify a specific product launch).
4. **Layer 5+ (Business Logic)**:
   * **Product Catalog**: Creation, versioning, and management of products.
   * **Launch Engine**: Workflows, tasks, timelines, calendar integrations, and tracking checklists for launching a product to market.
   * **Reporting Dashboard**: Insights into launch performance, team speed, and success metrics.
