from django.db import models
from common.models.base_model import BaseModel

class SIEMIntegrationConfig(BaseModel):
    """
    Configuration for an external SIEM provider.
    e.g. Splunk, Sentinel.
    """
    PROVIDER_CHOICES = [
        ('SPLUNK_HEC', 'Splunk HEC'),
        ('SENTINEL', 'Microsoft Sentinel'),
        ('WAZUH', 'Wazuh'),
    ]

    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES, unique=True)
    endpoint_url = models.URLField(max_length=1024, blank=True)
    is_active = models.BooleanField(default=False)
    
    # Optional filtering
    min_severity_to_forward = models.CharField(max_length=20, default='INFO')

    class Meta:
        db_table = "integrations_siem_config"

    def __str__(self):
        return f"{self.provider} ({'Active' if self.is_active else 'Inactive'})"


class SIEMRetryQueue(BaseModel):
    """
    Stores events/alerts that failed to forward to the external SIEM.
    """
    provider = models.CharField(max_length=50)
    payload = models.JSONField()
    retry_count = models.IntegerField(default=0)
    last_error = models.TextField(blank=True)
    next_retry_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "integrations_siem_retry_queue"
        ordering = ["next_retry_at"]

    def __str__(self):
        return f"Retry {self.id} for {self.provider}"
