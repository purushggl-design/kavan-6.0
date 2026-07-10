import pytest
from apps.siem.models.rules import DetectionRule, RuleType
from apps.incidents.models.incidents import Alert, AlertStatus, Incident
from apps.monitoring.models.events import Event
from apps.siem.services.engine import SIEMEngine

@pytest.mark.django_db
def test_siem_engine_triggers_alert_on_exact_match():
    # Setup Detection Rule
    rule = DetectionRule.objects.create(
        name="Suspicious Login",
        rule_type=RuleType.EXACT_MATCH,
        conditions={"event_type": "FAILED_LOGIN", "module": "Authentication"},
        severity="HIGH"
    )
    
    # Create matching event
    event = Event.objects.create(
        module="Authentication",
        event_type="FAILED_LOGIN",
        severity="MEDIUM",
        resource="User:123"
    )
    
    # Process through SIEM Engine
    SIEMEngine.analyze(event)
    
    # Verify Alert was created
    assert Alert.objects.count() == 1
    alert = Alert.objects.first()
    assert alert.title == "Detection Rule Triggered: Suspicious Login"
    assert alert.severity == "HIGH"
    assert alert.status == AlertStatus.NEW
    assert alert.rule_name == "Suspicious Login"

@pytest.mark.django_db
def test_siem_engine_ignores_non_matching_event():
    # Setup Detection Rule
    rule = DetectionRule.objects.create(
        name="Suspicious Login",
        rule_type=RuleType.EXACT_MATCH,
        conditions={"event_type": "FAILED_LOGIN"},
        severity="HIGH"
    )
    
    # Create NON-matching event
    event = Event.objects.create(
        module="Authentication",
        event_type="SUCCESSFUL_LOGIN",
        severity="INFO",
        resource="User:123"
    )
    
    SIEMEngine.analyze(event)
    
    # Verify NO Alert was created
    assert Alert.objects.count() == 0
