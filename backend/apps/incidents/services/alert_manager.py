import logging
from typing import Dict, Any, List
from apps.monitoring.models.events import EventSeverity
from apps.incidents.models.incidents import Alert
from .notification_engine import NotificationEngine

logger = logging.getLogger("kavan.apps.monitoring")

class AlertManager:
    """
    Handles generation and lifecycle of Alerts from the SIEM engine.
    """
    
    @classmethod
    def create_alert(cls, title: str, description: str, severity: str, rule_name: str = None, event_data: Dict[str, Any] = None, tenant_id=None) -> Alert:
        """
        Creates a new alert and optionally notifies if severity is high enough.
        """
        alert = Alert.objects.create(
            title=title,
            description=description,
            severity=severity,
            rule_name=rule_name,
            event_data=event_data or {},
            tenant_id=tenant_id
        )
        
        logger.warning(f"New Alert Generated: {title} [{severity}]")
        
        # Immediate notification for CRITICAL alerts
        if severity == EventSeverity.CRITICAL:
            engine = NotificationEngine()
            engine.notify(
                subject=f"CRITICAL ALERT: {title}",
                message=description,
                severity=severity,
                context={"alert_id": str(alert.id), "rule": rule_name}
            )
            
        return alert

    @classmethod
    def acknowledge_alert(cls, alert: Alert):
        from apps.incidents.models.incidents import AlertStatus
        alert.status = AlertStatus.ACKNOWLEDGED
        alert.save(update_fields=["status", "updated_at"])

    @classmethod
    def resolve_alert(cls, alert: Alert):
        from apps.incidents.models.incidents import AlertStatus
        alert.status = AlertStatus.RESOLVED
        alert.save(update_fields=["status", "updated_at"])
