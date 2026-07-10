import logging
from typing import Dict, Any, List
from apps.siem.models.rules import CorrelationRule
from apps.monitoring.models.events import Event
from apps.incidents.services.incident_manager import IncidentManager

logger = logging.getLogger("kavan.apps.siem")

class CorrelationEngine:
    """
    Evaluates sequences of events to detect complex attack patterns.
    """
    
    @classmethod
    def evaluate(cls, event: Event):
        """
        For a fully mature Correlation Engine, this would pull state from Redis.
        For MVP, we will evaluate active CorrelationRules and query the DB for the sequence.
        """
        active_rules = CorrelationRule.objects.filter(is_active=True)
        
        for rule in active_rules:
            try:
                cls._evaluate_rule(rule, event)
            except Exception as e:
                logger.error(f"Error evaluating correlation rule {rule.name}: {str(e)}")

    @classmethod
    def _evaluate_rule(cls, rule: CorrelationRule, current_event: Event):
        """
        Check if current_event is the LAST event in the sequence, then look backwards.
        """
        sequence = rule.sequence
        if not sequence:
            return
            
        last_condition = sequence[-1]
        
        # If the current event doesn't match the last step in the sequence, ignore
        if current_event.event_type != last_condition.get("event_type"):
            return
            
        # We need to query backwards in the time window for the remaining sequence.
        # This is a complex state-machine problem. 
        # For this prototype, we'll implement a basic naive lookup.
        # (A production SIEM uses streaming window correlation, e.g., Flink or Redis streams)
        
        # If it matches, we trigger an INCIDENT directly, since correlation rules are high-confidence.
        # cls._trigger_incident(rule, current_event)
        
        # Placeholder for actual correlation logic execution
        pass

    @classmethod
    def _trigger_incident(cls, rule: CorrelationRule, final_event: Event):
        IncidentManager.create_incident_from_alerts(
            title=f"Correlation Detected: {rule.name}",
            description=f"Complex sequence matched ending with {final_event.event_type}.",
            severity=rule.severity,
            alerts=[], # No alerts, generating incident directly
            tenant_id=final_event.tenant_id
        )
