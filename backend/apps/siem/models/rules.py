from django.db import models
from common.models.base_model import BaseModel
from apps.monitoring.models.events import EventSeverity

class RuleType(models.TextChoices):
    THRESHOLD = "THRESHOLD", "Threshold"
    EXACT_MATCH = "EXACT_MATCH", "Exact Match"
    ANOMALY = "ANOMALY", "Anomaly"

class DetectionRule(BaseModel):
    """
    Configurable detection rules stored in the database instead of hardcoding.
    Examples: Brute Force, Impossible Travel, Privilege Escalation.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    rule_type = models.CharField(max_length=50, choices=RuleType.choices, default=RuleType.THRESHOLD)
    
    # JSON conditions to match against the event
    # e.g., {"event_type": "FAILED_LOGIN"}
    conditions = models.JSONField(default=dict)
    
    # Threshold based detection
    threshold = models.IntegerField(default=1, help_text="Number of matches required to trigger an alert.")
    time_window_seconds = models.IntegerField(default=0, help_text="Time window for threshold-based rules (0 for instant).")
    
    severity = models.CharField(max_length=20, choices=EventSeverity.choices, default=EventSeverity.LOW)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "siem_detection_rule"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.get_severity_display()})"


class CorrelationRule(BaseModel):
    """
    Correlates related events.
    e.g., Login Failed -> Password Reset -> Admin Login -> Deployment Delete -> Threat Detected
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    
    # Sequence of event conditions to match in order
    sequence = models.JSONField(default=list)
    
    time_window_seconds = models.IntegerField(default=300, help_text="Max time window between first and last event.")
    severity = models.CharField(max_length=20, choices=EventSeverity.choices, default=EventSeverity.CRITICAL)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "siem_correlation_rule"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Correlation: {self.name}"
