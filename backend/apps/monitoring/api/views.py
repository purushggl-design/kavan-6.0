from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.monitoring.models.events import Event
from apps.monitoring.models.metrics import Metric, HealthCheck
from apps.monitoring.api.serializers import EventSerializer, MetricSerializer, HealthCheckSerializer
from apps.rbac.permissions.decorators import HasPlatformPermission

class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API for viewing system events (Layer 7).
    """
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, HasPlatformPermission("VIEW_SECURITY_EVENTS")()]
    queryset = Event.objects.all()

class MetricViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API for viewing system metrics (Layer 7).
    """
    serializer_class = MetricSerializer
    permission_classes = [IsAuthenticated, HasPlatformPermission("VIEW_METRICS")()]
    queryset = Metric.objects.all()

class HealthCheckViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API for viewing historical health checks.
    """
    serializer_class = HealthCheckSerializer
    permission_classes = [IsAuthenticated, HasPlatformPermission("VIEW_METRICS")()]
    queryset = HealthCheck.objects.all()

from rest_framework.views import APIView
from rest_framework.response import Response

class PlatformDashboardAPIView(APIView):
    """
    High-level platform metrics for operations.
    """
    permission_classes = [IsAuthenticated, HasPlatformPermission("VIEW_METRICS")()]

    def get(self, request):
        return Response({
            "status": "healthy",
            "active_tenants": 0,
            "total_deployments": 0,
            "active_alerts": 0
        })

class SOCDashboardAPIView(APIView):
    """
    Security Operations Center dashboard metrics.
    """
    permission_classes = [IsAuthenticated, HasPlatformPermission("VIEW_SECURITY_EVENTS")()]

    def get(self, request):
        try:
            from apps.incidents.models.incidents import Incident, Alert
            active_incidents = Incident.objects.exclude(status="CLOSED").count()
            unacked_alerts = Alert.objects.filter(status="NEW").count()
        except Exception:
            active_incidents = 0
            unacked_alerts = 0
            
        return Response({
            "active_incidents": active_incidents,
            "unacknowledged_alerts": unacked_alerts,
            "recent_threats": []
        })

class TenantDashboardAPIView(APIView):
    """
    Tenant-specific monitoring dashboard.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, tenant_id):
        return Response({
            "tenant_id": tenant_id,
            "deployments_running": 0,
            "failed_events_24h": 0
        })
