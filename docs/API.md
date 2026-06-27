# KAVAN v6.0 — API Reference

## Standard Response Format

All API endpoints return a consistent JSON envelope:

### Success Response
```json
{
    "success": true,
    "message": "Operation successful.",
    "data": { },
    "errors": null,
    "meta": {
        "timestamp": "2026-06-26T10:30:00.123Z",
        "request_id": "550e8400-e29b-41d4-a716-446655440000",
        "version": "v1"
    }
}
```

### Error Response
```json
{
    "success": false,
    "message": "Validation failed.",
    "data": null,
    "errors": [
        {
            "field": "email",
            "code": "INVALID_EMAIL",
            "message": "Please enter a valid email address."
        }
    ],
    "meta": {
        "timestamp": "2026-06-26T10:30:00.123Z",
        "request_id": "550e8400-e29b-41d4-a716-446655440000",
        "version": "v1"
    }
}
```

### Paginated Response
```json
{
    "success": true,
    "message": "Data retrieved successfully.",
    "data": [],
    "errors": null,
    "meta": {
        "timestamp": "...",
        "request_id": "...",
        "version": "v1",
        "pagination": {
            "page": 1,
            "page_size": 20,
            "total_count": 150,
            "total_pages": 8,
            "has_next": true,
            "has_previous": false,
            "next_url": "http://api/v1/resource/?page=2",
            "previous_url": null
        }
    }
}
```

---

## Health Check Endpoints

### `GET /health/`
Full health check — all services.

**Response (200 OK):**
```json
{
    "success": true,
    "message": "All systems operational.",
    "data": {
        "status": "healthy",
        "uptime_seconds": 3600.5,
        "services": {
            "database": { "status": "ok", "latency_ms": 2.1, "message": "..." },
            "redis":    { "status": "ok", "latency_ms": 0.5, "message": "..." },
            "celery":   { "status": "ok", "latency_ms": 45.2, "details": { "worker_count": 2 } }
        }
    },
    "errors": null,
    "meta": { "timestamp": "...", "request_id": "...", "version": "v1" }
}
```

**Response (503 Service Unavailable):** When DB or Redis is down.

---

### `GET /health/live/`
Kubernetes liveness probe.

**Response (200 OK):**
```json
{ "status": "alive", "timestamp": "...", "uptime_seconds": 3600.5 }
```

---

### `GET /health/ready/`
Kubernetes readiness probe.

**Response (200 OK):**
```json
{ "status": "ready", "database": true, "redis": true, "timestamp": "..." }
```

**Response (503):**
```json
{ "status": "not_ready", "database": false, "redis": true, "timestamp": "..." }
```

---

### `GET /health/db/`
Database health only.

### `GET /health/redis/`
Redis health only.

### `GET /health/celery/`
Celery worker health.

---

## API Versioning

```
/api/v1/...    Current version
/api/v2/...    Future version
```

Pass `X-Request-ID` header to correlate requests across services.

---

## Error Codes

| Code | HTTP | Description |
|------|------|-------------|
| `AUTHENTICATION_FAILED` | 401 | Invalid/missing credentials |
| `TOKEN_EXPIRED` | 401 | JWT/session expired |
| `PERMISSION_DENIED` | 403 | Insufficient permissions |
| `RESOURCE_NOT_FOUND` | 404 | Resource doesn't exist |
| `VALIDATION_ERROR` | 422 | Input validation failed |
| `DUPLICATE_VALUE` | 409 | Unique constraint violation |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Unexpected server error |
| `SERVICE_UNAVAILABLE` | 503 | Dependency unavailable |
