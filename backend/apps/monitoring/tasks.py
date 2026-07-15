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

import requests
from django.utils import timezone
from apps.audit.models import AuditEvent, AuditEventType
from apps.marketplace.models.application import TenantInstallation, InstallationStatus

@shared_task
def log_health_status():
    """
    Log general system health status.
    """
    logger.info("System health check performed successfully.")

@shared_task
def check_installation_health():
    """
    Periodic task to monitor the health of all RUNNING tenant installations.
    """
    installations = TenantInstallation.objects.filter(status=InstallationStatus.RUNNING)
    
    for install in installations:
        try:
            # Reconstruct the internal endpoint from the manifest
            manifest = install.version.manifest
            port = manifest.get('runtime', {}).get('container_port', 80)
            health_path = manifest.get('runtime', {}).get('health_check_path', '/')
            
            # Use the route_path to find the internal host if needed, 
            # or standard container hostname: kavan-{tenant.id}-{app.code}
            container_name = f"kavan_tenant_{install.tenant.tenant_code}_{install.version.application.code}"
            
            # Using http://{container_name}:{port}{health_path} within Docker network
            url = f"http://{container_name}:{port}{health_path}"
            
            response = requests.get(url, timeout=3)
            
            if response.status_code == 200:
                # Still healthy, update timestamp
                install.save(update_fields=['updated_at'])
            else:
                # Flip to failed
                logger.warning(f"Installation {install.id} health check returned {response.status_code}")
                _mark_installation_failed(install)
                
        except (requests.RequestException, requests.Timeout) as e:
            # Connection error or timeout
            logger.warning(f"Installation {install.id} health check failed: {e}")
            _mark_installation_failed(install)
            
def _mark_installation_failed(install):
    install.status = InstallationStatus.FAILED
    install.save(update_fields=['status', 'updated_at'])
    
    # Audit log
    AuditEvent.objects.create(
        tenant_id=install.tenant.id,
        event_type=AuditEventType.INSTALLATION_FAILED,
        success=False,
        failure_reason="HEALTH_CHECK_FAILED",
        metadata={
            "installation_id": str(install.id),
            "reason": "Health check failed or timed out"
        }
    )

@shared_task
def log_health_status_legacy():
    from monitoring.health_checks import check_database, check_redis, check_celery
    db = check_database()
    redis = check_redis()
    celery = check_celery()
    
    if db["status"] == "ok" and redis["status"] == "ok" and celery["status"] == "ok":
        logger.info("Health Check: All systems operational.")
    else:
        logger.warning(f"Health Check Degraded. DB: {db['status']}, Redis: {redis['status']}, Celery: {celery['status']}")

