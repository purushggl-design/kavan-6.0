"""
KAVAN v6.0 — Health App Tasks (Celery)
"""

import logging

from config.celery import app

logger = logging.getLogger("kavan")


@app.task(name="apps.health.tasks.log_health_status", bind=True, ignore_result=True)
def log_health_status(self):
    """
    Periodic task to log health status.
    Runs every 5 minutes via Celery Beat.
    """
    from monitoring.health_checks import check_database, check_redis, check_celery

    db = check_database()
    redis = check_redis()
    celery = check_celery()

    logger.info(
        "Scheduled health check",
        extra={
            "kavan_data": {
                "database": db,
                "redis": redis,
                "celery": celery,
            }
        },
    )
