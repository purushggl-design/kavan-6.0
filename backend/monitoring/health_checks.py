"""
KAVAN v6.0 — Health Check Functions
============================================================
Low-level service health checks used by:
  - /health/ views
  - Celery beat scheduled tasks
  - Monitoring module probes

Each check returns:
{
    "status": "ok" | "error",
    "latency_ms": float,
    "message": str,
    "details": dict (optional)
}
"""

import logging
import time
from typing import Dict, Any

logger = logging.getLogger("kavan")


def check_database() -> Dict[str, Any]:
    """
    Check PostgreSQL database connectivity.
    Runs a simple SELECT 1 query via Django ORM.
    """
    start = time.monotonic()
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        latency_ms = round((time.monotonic() - start) * 1000, 2)
        return {
            "status": "ok",
            "latency_ms": latency_ms,
            "message": "Database is reachable.",
        }
    except Exception as exc:
        latency_ms = round((time.monotonic() - start) * 1000, 2)
        logger.error(f"Database health check failed: {exc}", exc_info=True)
        return {
            "status": "error",
            "latency_ms": latency_ms,
            "message": f"Database connection failed: {str(exc)}",
        }


def check_redis() -> Dict[str, Any]:
    """
    Check Redis connectivity by sending a PING command.
    """
    start = time.monotonic()
    try:
        from django.core.cache import cache
        cache.set("_health_check_probe_", "ok", timeout=10)
        value = cache.get("_health_check_probe_")
        latency_ms = round((time.monotonic() - start) * 1000, 2)

        if value == "ok":
            return {
                "status": "ok",
                "latency_ms": latency_ms,
                "message": "Redis is reachable.",
            }
        return {
            "status": "error",
            "latency_ms": latency_ms,
            "message": "Redis ping failed (unexpected value).",
        }
    except Exception as exc:
        latency_ms = round((time.monotonic() - start) * 1000, 2)
        logger.error(f"Redis health check failed: {exc}", exc_info=True)
        return {
            "status": "error",
            "latency_ms": latency_ms,
            "message": f"Redis connection failed: {str(exc)}",
        }


def check_celery() -> Dict[str, Any]:
    """
    Check Celery worker availability by inspecting active workers.
    Returns 'degraded' (not 'error') if no workers are found,
    since Celery is not critical for Layer 1.
    """
    start = time.monotonic()
    try:
        from config.celery import app as celery_app
        inspect = celery_app.control.inspect(timeout=2.0)
        active_workers = inspect.active()
        latency_ms = round((time.monotonic() - start) * 1000, 2)

        if active_workers:
            worker_count = len(active_workers)
            return {
                "status": "ok",
                "latency_ms": latency_ms,
                "message": f"{worker_count} worker(s) active.",
                "details": {"worker_count": worker_count},
            }
        else:
            return {
                "status": "degraded",
                "latency_ms": latency_ms,
                "message": "No active Celery workers found.",
                "details": {"worker_count": 0},
            }
    except Exception as exc:
        latency_ms = round((time.monotonic() - start) * 1000, 2)
        logger.warning(f"Celery health check failed: {exc}")
        return {
            "status": "degraded",
            "latency_ms": latency_ms,
            "message": f"Celery health check failed: {str(exc)}",
        }


def get_full_health_report() -> Dict[str, Any]:
    """Run all health checks and return a consolidated report."""
    db = check_database()
    redis = check_redis()
    celery = check_celery()

    critical_ok = db["status"] == "ok" and redis["status"] == "ok"

    return {
        "overall": "healthy" if critical_ok else "degraded",
        "critical": critical_ok,
        "services": {
            "database": db,
            "redis": redis,
            "celery": celery,
        },
    }
