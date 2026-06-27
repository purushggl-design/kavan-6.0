# KAVAN v6.0 — Architecture Documentation

This document describes the design architecture, layer mapping, and structural layout of KAVAN v6.0.

---

## 1. Clean Architecture Layers

KAVAN is built using clean architecture boundaries designed to preserve a high degree of decoupling. The application enforces a strict separation between controllers, interfaces, business processes, and data access.

```mermaid
graph TD
    subgraph Client Space
        UA[User Agent / Web App]
        LB[Nginx Reverse Proxy]
    end

    subgraph Django Application HTTP Layer
        RL[Request Logging Middleware]
        ID[Request ID / Correlation Middleware]
        SH[Security Hardening Middleware]
        DRF[Django REST Framework View]
    end

    subgraph Dependency Injection IoC Space
        SC[ServiceContainer]
        RP[RepositoryProvider]
        SP[ServiceProvider]
    end

    subgraph Business Logic Layer
        BS[Concrete Service / IService]
    end

    subgraph Data & Storage Layer
        BR[Concrete Repository / IRepository]
        ORM[Django ORM / Models]
        DB[(PostgreSQL Database)]
        RD[(Redis Cache)]
    end

    UA -->|HTTP Request| LB
    LB -->|Forwarded Headers| RL
    RL --> ID
    ID --> SH
    SH --> DRF
    DRF -->|Resolves Service| SP
    SP -->|Injects| BS
    BS -->|Resolves Repo| RP
    RP -->|Uses| BR
    BR -->|Queries| ORM
    ORM --> DB
    ORM --> RD
```

---

## 2. Request Processing Flow (Sequence)

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant Proxy as Nginx Proxy
    participant Middle as Middleware Chain
    participant Controller as DRF View (Controller)
    participant Container as IoC Service Container
    participant Service as Service Layer
    participant Repo as Repository Layer
    participant DB as Postgres/Redis

    Client->>Proxy: GET /api/v1/health/system/
    Proxy->>Middle: Forward Request (X-Request-ID, X-Correlation-ID)
    Note over Middle: Correlation ID & RequestContext initialized
    Middle->>Controller: Routed Request
    Controller->>Container: ServiceProvider.get_service(SystemHealthView)
    Container->>Service: Instantiate with dependencies
    Service->>Repo: RepositoryProvider.get_repository(Model)
    Repo->>DB: Query or fetch metrics
    DB-->>Repo: Data Snapshot
    Repo-->>Service: Return clean Entity
    Service-->>Controller: Return Business Result
    Controller-->>Middle: Construct StandardResponse success()
    Note over Middle: Log Request Details (redacted PII) & clear Context
    Middle-->>Proxy: Return JSON response + headers
    Proxy-->>Client: Payload delivered
```

---

## 3. Deployment Topology

```mermaid
flowchart LR
    LB[Nginx SSL termination] -->|Reverse Proxy / Unix Socket| Gunicorn[Gunicorn Worker Pool]
    Gunicorn -->|Django Application| DB[(PostgreSQL Master)]
    Gunicorn -->|Caching / Session| Redis[(Redis Primary)]
    Celery[Celery Task Workers] -->|Broker| Redis
    Celery -->|Write Operations| DB
```
