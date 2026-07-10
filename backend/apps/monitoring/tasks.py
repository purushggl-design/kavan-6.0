import logging
from celery import shared_task
from apps.monitoring.models.events import Event

logger = logging.getLogger("kavan")

@shared_task
def process_event_task(payload: dict):
    """
    Consumes events from the Event Bus queue (Redis) and processes them.
    Currently persists the event to the database.
    In Phase 2, this will also forward to the SIEM Engine for correlation.
    """
    try:
        event = Event.objects.create(
            module=payload.get("module"),
            event_type=payload.get("event_type"),
            action=payload.get("action"),
            status=payload.get("status"),
            severity=payload.get("severity"),
            tenant_id=payload.get("tenant_id"),
            user_id=payload.get("user_id"),
            resource=payload.get("resource"),
            metadata=payload.get("metadata", {})
        )
        logger.debug(f"Event persisted: {event.id}")
        
        # Phase 2: Forward to SIEM Engine for threat detection and correlation
        try:
            from apps.siem.services.engine import SIEMEngine
            SIEMEngine.analyze(event)
        except Exception as e:
            logger.error(f"SIEM Engine failed to process event {event.id}: {str(e)}")
            
        return str(event.id)
    except Exception as e:
        logger.error(f"Failed to process event from bus: {str(e)}")
        raise

@shared_task
def log_health_status():
    from monitoring.health_checks import check_database, check_redis, check_celery
    db = check_database()
    redis = check_redis()
    celery = check_celery()
    
    if db["status"] == "ok" and redis["status"] == "ok" and celery["status"] == "ok":
        logger.info("Health Check: All systems operational.")
    else:
        logger.warning(f"Health Check Degraded. DB: {db['status']}, Redis: {redis['status']}, Celery: {celery['status']}")

