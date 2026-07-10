import logging
import json
from typing import Dict, Any, List
from django.utils import timezone
from datetime import timedelta
from apps.siem.models.rules import DetectionRule, RuleType
from apps.monitoring.models.events import Event
from apps.incidents.services.alert_manager import AlertManager

logger = logging.getLogger("kavan.apps.siem")

class DetectionEngine:
    """
    Evaluates incoming normalized events against active detection rules.
    """
    
    @classmethod
    def evaluate(cls, event: Event):
        """
        Run the event through all active detection rules.
        """
        active_rules = DetectionRule.objects.filter(is_active=True)
        
        for rule in active_rules:
            try:
                cls._evaluate_rule(rule, event)
            except Exception as e:
                logger.error(f"Error evaluating rule {rule.name}: {str(e)}")

    @classmethod
    def _evaluate_rule(cls, rule: DetectionRule, event: Event):
        """
        Evaluates a single rule against an event.
        """
        # 1. Check conditions
        if not cls._matches_conditions(rule.conditions, event):
            return

        # 2. Match found. Determine if threshold is met.
        if rule.rule_type == RuleType.EXACT_MATCH:
            cls._trigger_alert(rule, [event])
            return
            
        elif rule.rule_type == RuleType.THRESHOLD:
            # We need to query recent events matching these conditions
            if rule.time_window_seconds > 0:
                time_threshold = timezone.now() - timedelta(seconds=rule.time_window_seconds)
                
                # Query past events matching the exact condition in the time window
                # For simplicity, we just check how many events of this type for this user/tenant exist
                # A robust SIEM would use a specialized search backend (Elastic) or a Redis counter.
                recent_count = Event.objects.filter(
                    event_type=event.event_type,
                    tenant_id=event.tenant_id,
                    user_id=event.user_id,
                    timestamp__gte=time_threshold
                ).count()
                
                if recent_count >= rule.threshold:
                    # To prevent alert fatigue, we should ideally debounce, but for now we trigger
                    cls._trigger_alert(rule, [event])
                    
            else:
                # If window is 0, just trigger
                cls._trigger_alert(rule, [event])


    @classmethod
    def _matches_conditions(cls, conditions: dict, event: Event) -> bool:
        """
        Simple key-value matching. 
        e.g. conditions = {"event_type": "FAILED_LOGIN"}
        """
        if not conditions:
            return False
            
        event_dict = {
            "event_type": event.event_type,
            "action": event.action,
            "status": event.status,
            "module": event.module
        }
        
        for key, value in conditions.items():
            if event_dict.get(key) != value:
                return False
        return True

    @classmethod
    def _trigger_alert(cls, rule: DetectionRule, events: List[Event]):
        """
        Dispatches to AlertManager.
        """
        latest_event = events[-1]
        
        AlertManager.create_alert(
            title=f"Detection Rule Triggered: {rule.name}",
            description=f"Rule '{rule.name}' matched for tenant {latest_event.tenant_id} on resource {latest_event.resource}.",
            severity=rule.severity,
            rule_name=rule.name,
            event_data={"event_id": str(latest_event.id), "type": latest_event.event_type},
            tenant_id=latest_event.tenant_id
        )
