from django.db import models
from common.models.base_model import BaseModel

class MetricType(models.TextChoices):
    CPU = "CPU", "CPU Usage"
    RAM = "RAM", "RAM Usage"
    DISK = "DISK", "Disk Usage"
    NETWORK = "NETWORK", "Network Traffic"
    DATABASE = "DATABASE", "Database Metrics"
    REDIS = "REDIS", "Redis Metrics"
    CELERY = "CELERY", "Celery Queue"
    DOCKER = "DOCKER", "Docker Metrics"
    CUSTOM = "CUSTOM", "Custom Metric"

class Metric(BaseModel):
    """
    Stores system metrics collected by the Metrics Engine.
    """
    tenant_id = models.UUIDField(null=True, blank=True, db_index=True)
    metric_type = models.CharField(max_length=50, choices=MetricType.choices, db_index=True)
    name = models.CharField(max_length=100) # e.g. cpu_percent, memory_used_mb
    value = models.FloatField()
    unit = models.CharField(max_length=20) # e.g. %, MB, count, ms
    tags = models.JSONField(default=dict, blank=True) # e.g. {"container": "api_1"}

    class Meta:
        db_table = "monitoring_metrics"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.metric_type} - {self.name}: {self.value}{self.unit}"


class HealthStatus(models.TextChoices):
    HEALTHY = "HEALTHY", "Healthy"
    WARNING = "WARNING", "Warning"
    CRITICAL = "CRITICAL", "Critical"

class HealthCheck(BaseModel):
    """
    Historical record of system component health checks.
    """
    service_name = models.CharField(max_length=100, db_index=True) # API, PostgreSQL, Redis, Celery, Docker
    status = models.CharField(max_length=20, choices=HealthStatus.choices)
    latency_ms = models.FloatField(null=True, blank=True)
    details = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "monitoring_health_checks"
        ordering = ["-created_at"]

    def __str__(self):
        return f"HealthCheck: {self.service_name} [{self.status}]"
