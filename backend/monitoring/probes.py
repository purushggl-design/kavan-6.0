"""
KAVAN v6.0 — Liveness and Readiness Probes
============================================================
Higher-level probe classes that encapsulate the logic
for Kubernetes-style health probes.
"""

from monitoring.health_checks import check_database, check_redis, check_celery


class LivenessProbe:
    """
    Liveness probe — is the application process alive?

    A failing liveness probe causes Kubernetes to restart the pod.
    Should only fail for truly unrecoverable errors.
    """

    def check(self) -> dict:
        """Return liveness status."""
        import time
        return {
            "alive": True,
            "timestamp": time.time(),
        }


class ReadinessProbe:
    """
    Readiness probe — is the application ready to serve traffic?

    A failing readiness probe removes the pod from the load balancer.
    Should fail when required services (DB, cache) are unavailable.
    """

    def check(self) -> dict:
        """
        Check readiness by verifying critical services.
        Returns True only if database AND redis are reachable.
        """
        db = check_database()
        redis = check_redis()

        db_ok = db["status"] == "ok"
        redis_ok = redis["status"] == "ok"
        ready = db_ok and redis_ok

        return {
            "ready": ready,
            "database": db_ok,
            "redis": redis_ok,
            "services": {
                "database": db,
                "redis": redis,
            },
        }


class StartupProbe:
    """
    Startup probe — has the application finished initializing?

    Used to give slow-starting containers more time before
    liveness/readiness probes take over.
    """

    def check(self) -> dict:
        """Check if startup is complete (database migrations run)."""
        try:
            from django.db import connection
            from django.db.migrations.executor import MigrationExecutor

            executor = MigrationExecutor(connection)
            plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
            migrations_pending = len(plan) > 0

            return {
                "started": not migrations_pending,
                "migrations_pending": migrations_pending,
            }
        except Exception as exc:
            return {
                "started": False,
                "error": str(exc),
            }
