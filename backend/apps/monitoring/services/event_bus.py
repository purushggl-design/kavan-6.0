import logging
from typing import Optional, Dict, Any
from uuid import UUID

from django.utils import timezone
from apps.monitoring.models.events import EventSeverity

logger = logging.getLogger("kavan")

class EventBusService:
    """
    Centralized Event Bus for KAVAN.
    All modules (Auth, Deployment, RBAC) publish events here.
    """

    @classmethod
    def publish(
        cls,
        module: str,
        event_type: str,
        action: str,
        status: str,
        severity: str = EventSeverity.INFO,
        tenant_id: Optional[UUID] = None,
        user_id: Optional[UUID] = None,
        resource: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Publish an event to the Event Bus asynchronously via Celery.
        """
        from apps.monitoring.tasks import process_event_task

        payload = {
            "module": module,
            "event_type": event_type,
            "action": action,
            "status": status,
            "severity": severity,
            "tenant_id": str(tenant_id) if tenant_id else None,
            "user_id": str(user_id) if user_id else None,
            "resource": resource,
            "metadata": metadata or {},
            "timestamp": timezone.now().isoformat()
        }

        # Dispatch to Celery queue
        process_event_task.delay(payload)
        logger.debug(f"Event published to bus: {module} | {event_type}")
