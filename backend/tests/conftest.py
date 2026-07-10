import pytest
from unittest.mock import patch

@pytest.fixture(autouse=True)
def mock_event_bus_globally(request):
    """Globally mock EventBusService.publish so tests don't require Redis."""
    if "monitoring" in request.node.nodeid:
        yield
    else:
        with patch("apps.monitoring.services.event_bus.EventBusService.publish") as mock_publish:
            yield mock_publish
