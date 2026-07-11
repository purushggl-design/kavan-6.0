"""
KAVAN v6.0 — Health Check Views
============================================================
Provides endpoints for Kubernetes/Docker liveness and readiness
probes, plus full application health status.

Endpoints:
  GET /health/         → Full health (DB + Redis + Celery)
  GET /health/live/    → Liveness probe (process alive)
  GET /health/ready/   → Readiness probe (services reachable)
  GET /health/db/      → Database health
  GET /health/redis/   → Redis health
  GET /health/celery/  → Celery health
"""

import logging
import time
from datetime import datetime, timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request

from monitoring.health_checks import check_database, check_redis, check_celery

logger = logging.getLogger("kavan")

# Application start time for uptime calculation
_START_TIME = time.time()


def _get_uptime() -> float:
    """Return application uptime in seconds."""
    return round(time.time() - _START_TIME, 2)


from drf_spectacular.utils import extend_schema

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class HealthView(APIView):
    """
    GET /health/

    Full health check — checks database, Redis, and Celery.
    Returns aggregate status and individual service statuses.
    """

    authentication_classes = []
    permission_classes = []

    @extend_schema(exclude=True)
    def get(self, request: Request) -> Response:
        db_result = check_database()
        redis_result = check_redis()
        celery_result = check_celery()

        all_healthy = all([
            db_result["status"] == "ok",
            redis_result["status"] == "ok",
        ])

        response_status = status.HTTP_200_OK if all_healthy else status.HTTP_503_SERVICE_UNAVAILABLE

        return Response(
            {
                "success": all_healthy,
                "message": "All systems operational." if all_healthy else "Some services are degraded.",
                "data": {
                    "status": "healthy" if all_healthy else "degraded",
                    "uptime_seconds": _get_uptime(),
                    "services": {
                        "database": db_result,
                        "redis": redis_result,
                        "celery": celery_result,
                    },
                },
                "errors": None,
                "meta": {
                    "timestamp": _now_iso(),
                    "request_id": getattr(request, "request_id", ""),
                    "version": "v1",
                },
            },
            status=response_status,
        )


class LivenessView(APIView):
    """
    GET /health/live/

    Kubernetes liveness probe.
    Returns 200 if the Django process is alive.
    Returns 503 only if the process is in a crash-loop.
    """

    authentication_classes = []
    permission_classes = []

    @extend_schema(exclude=True)
    def get(self, request: Request) -> Response:
        return Response(
            {
                "status": "alive",
                "timestamp": _now_iso(),
                "uptime_seconds": _get_uptime(),
            },
            status=status.HTTP_200_OK,
        )


class ReadinessView(APIView):
    """
    GET /health/ready/

    Kubernetes readiness probe.
    Returns 200 only when all critical services are reachable.
    Load balancer will stop sending traffic if this returns non-2xx.
    """

    authentication_classes = []
    permission_classes = []

    @extend_schema(exclude=True)
    def get(self, request: Request) -> Response:
        db_result = check_database()
        redis_result = check_redis()

        db_ok = db_result["status"] == "ok"
        redis_ok = redis_result["status"] == "ok"
        ready = db_ok and redis_ok

        response_status = status.HTTP_200_OK if ready else status.HTTP_503_SERVICE_UNAVAILABLE

        return Response(
            {
                "status": "ready" if ready else "not_ready",
                "database": db_ok,
                "redis": redis_ok,
                "timestamp": _now_iso(),
            },
            status=response_status,
        )


class DatabaseHealthView(APIView):
    """
    GET /health/db/

    Database-specific health check.
    """

    authentication_classes = []
    permission_classes = []

    @extend_schema(exclude=True)
    def get(self, request: Request) -> Response:
        result = check_database()
        is_ok = result["status"] == "ok"
        response_status = status.HTTP_200_OK if is_ok else status.HTTP_503_SERVICE_UNAVAILABLE

        return Response(
            {
                "service": "database",
                **result,
                "timestamp": _now_iso(),
            },
            status=response_status,
        )


class RedisHealthView(APIView):
    """
    GET /health/redis/

    Redis-specific health check.
    """

    authentication_classes = []
    permission_classes = []

    @extend_schema(exclude=True)
    def get(self, request: Request) -> Response:
        result = check_redis()
        is_ok = result["status"] == "ok"
        response_status = status.HTTP_200_OK if is_ok else status.HTTP_503_SERVICE_UNAVAILABLE

        return Response(
            {
                "service": "redis",
                **result,
                "timestamp": _now_iso(),
            },
            status=response_status,
        )


class CeleryHealthView(APIView):
    """
    GET /health/celery/

    Celery worker health check.
    """

    authentication_classes = []
    permission_classes = []

    @extend_schema(exclude=True)
    def get(self, request: Request) -> Response:
        result = check_celery()
        is_ok = result["status"] == "ok"
        response_status = status.HTTP_200_OK if is_ok else status.HTTP_503_SERVICE_UNAVAILABLE

        return Response(
            {
                "service": "celery",
                **result,
                "timestamp": _now_iso(),
            },
            status=response_status,
        )
