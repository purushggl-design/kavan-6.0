import pytest
import responses
from django.utils import timezone
from apps.integrations.siem.providers.splunk import SplunkHECProvider
from apps.integrations.siem.connector import SIEMConnector
from apps.integrations.models.siem import SIEMIntegrationConfig, SIEMRetryQueue
from apps.monitoring.models.events import Event

@pytest.mark.django_db
@responses.activate
def test_splunk_hec_provider_normalization():
    event = Event.objects.create(
        module="RBAC",
        event_type="PRIVILEGE_ESCALATION",
        severity="CRITICAL",
        action="escalate",
        status="success",
        metadata={"ip_address": "192.168.1.100"}
    )
    
    provider = SplunkHECProvider("http://splunk.local/services/collector")
    provider.hec_token = "fake-token"
    
    payload = provider.normalize_event(event)
    
    assert payload["module"] == "RBAC"
    assert payload["mitre_tactic"] == "Privilege Escalation"
    assert payload["mitre_technique"] == "T1078"
    assert payload["src_ip"] == "192.168.1.100"

@pytest.mark.django_db
@responses.activate
def test_siem_connector_retry_queue():
    import os
    os.environ["SPLUNK_HEC_TOKEN"] = "fake-token"
    config = SIEMIntegrationConfig.objects.create(
        provider="SPLUNK_HEC",
        endpoint_url="http://splunk.local/services/collector",
        is_active=True
    )
    
    event = Event.objects.create(
        module="Authentication",
        event_type="FAILED_LOGIN",
        severity="HIGH"
    )
    
    # Mocking Splunk endpoint to return 500 error
    responses.add(responses.POST, "http://splunk.local/services/collector", status=500)
    
    # Act
    SIEMConnector.forward_event(event)
    
    # Assert
    # Since Splunk failed, the event should be in the retry queue
    assert SIEMRetryQueue.objects.count() == 1
    retry_item = SIEMRetryQueue.objects.first()
    assert retry_item.provider == "SPLUNK_HEC"
    assert retry_item.payload["module"] == "Authentication"
