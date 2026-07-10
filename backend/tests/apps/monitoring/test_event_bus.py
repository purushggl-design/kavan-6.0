import pytest
from unittest.mock import patch
from apps.monitoring.services.event_bus import EventBusService
from apps.monitoring.models.events import Event, EventSeverity
from apps.monitoring.tasks import process_event_task

@pytest.mark.django_db
class TestEventBusService:
    def test_publish_dispatches_task(self):
        with patch("apps.monitoring.tasks.process_event_task.delay") as mock_delay:
            EventBusService.publish(
                module="Authentication",
                event_type="Login Success",
                action="login",
                status="success",
                severity=EventSeverity.INFO,
            )
            mock_delay.assert_called_once()
            args, kwargs = mock_delay.call_args
            payload = args[0]
            assert payload["module"] == "Authentication"
            assert payload["event_type"] == "Login Success"
            assert payload["action"] == "login"
            assert payload["status"] == "success"
            assert payload["severity"] == EventSeverity.INFO

    def test_process_event_task_creates_db_record(self):
        payload = {
            "module": "Deployment",
            "event_type": "Deployment Started",
            "action": "create",
            "status": "pending",
            "severity": EventSeverity.MEDIUM,
            "metadata": {"container": "nginx"},
            "tenant_id": None,
            "user_id": None,
            "resource": "dep-123",
        }
        process_event_task(payload)
        
        event = Event.objects.first()
        assert event is not None
        assert event.module == "Deployment"
        assert event.event_type == "Deployment Started"
        assert event.action == "create"
        assert event.severity == EventSeverity.MEDIUM
        assert event.metadata == {"container": "nginx"}
