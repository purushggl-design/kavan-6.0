from django.db import models
from common.models.base_model import BaseModel

class EventSeverity(models.TextChoices):
    INFO = "INFO", "Info"
    LOW = "LOW", "Low"
    MEDIUM = "MEDIUM", "Medium"
    HIGH = "HIGH", "High"
    CRITICAL = "CRITICAL", "Critical"

class EventType(models.TextChoices):
    LOGIN = "LOGIN", "Login Success"
    LOGOUT = "LOGOUT", "Logout"
    FAILED_LOGIN = "FAILED_LOGIN", "Failed Login"
    DEPLOYMENT_STARTED = "DEPLOYMENT_STARTED", "Deployment Started"
    DEPLOYMENT_FAILED = "DEPLOYMENT_FAILED", "Deployment Failed"
    DEPLOYMENT_SUCCESS = "DEPLOYMENT_SUCCESS", "Deployment Success"
    RBAC_DENIED = "RBAC_DENIED", "RBAC Denied"
    PRODUCT_PUBLISHED = "PRODUCT_PUBLISHED", "Product Published"
    TENANT_CREATED = "TENANT_CREATED", "Tenant Created"
    USER_CREATED = "USER_CREATED", "User Created"
    SYSTEM_ALERT = "SYSTEM_ALERT", "System Alert"

class Event(BaseModel):
    """
    Standardized Event schema for the Event Bus.
    All system actions generate an event matching this schema.
    """
    tenant_id = models.UUIDField(null=True, blank=True, db_index=True)
    user_id = models.UUIDField(null=True, blank=True, db_index=True)
    module = models.CharField(max_length=100, db_index=True)
    event_type = models.CharField(max_length=50, choices=EventType.choices, db_index=True)
    severity = models.CharField(
        max_length=20, choices=EventSeverity.choices, default=EventSeverity.INFO, db_index=True
    )
    resource = models.CharField(max_length=255, null=True, blank=True)
    action = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "monitoring_events"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.module} | {self.event_type} | {self.severity} | {self.status}"
