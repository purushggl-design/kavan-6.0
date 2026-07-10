import logging
from typing import List
from apps.monitoring.models.events import EventSeverity
from apps.incidents.models.incidents import Alert, Incident, IncidentActivity, IncidentStatus
from .notification_engine import NotificationEngine

logger = logging.getLogger("kavan.apps.monitoring")

class IncidentManager:
    """
    Manages the lifecycle of high-level Incidents, grouping alerts.
    """
    
    @classmethod
    def create_incident_from_alerts(cls, title: str, description: str, severity: str, alerts: List[Alert], tenant_id=None, creator_user=None) -> Incident:
        """
        Creates an incident linking to one or more alerts.
        """
        incident = Incident.objects.create(
            title=title,
            description=description,
            severity=severity,
            tenant_id=tenant_id
        )
        
        if alerts:
            incident.alerts.add(*alerts)
            
        IncidentActivity.objects.create(
            incident=incident,
            user=creator_user,
            action="Created",
            notes="Incident automatically opened from alerts." if not creator_user else "Manually created."
        )
        
        logger.warning(f"New Incident Created: {title} [{severity}]")
        
        # Notify SOC team
        engine = NotificationEngine()
        engine.notify(
            subject=f"NEW INCIDENT: {title}",
            message=description,
            severity=severity,
            context={"incident_id": str(incident.id)}
        )
        
        return incident

    @classmethod
    def transition_status(cls, incident: Incident, new_status: str, user, notes: str = ""):
        """
        Safely transitions an incident to a new status and logs activity.
        """
        old_status = incident.status
        incident.status = new_status
        incident.save(update_fields=["status", "updated_at"])
        
        IncidentActivity.objects.create(
            incident=incident,
            user=user,
            action=f"Status changed from {old_status} to {new_status}",
            notes=notes
        )
        logger.info(f"Incident {incident.id} transitioned to {new_status}")
