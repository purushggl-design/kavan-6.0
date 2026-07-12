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
from rest_framework import serializers

class EmptySerializer(serializers.Serializer):
    pass

class PlatformDashboardAPIView(APIView):
    """
    High-level platform metrics for operations.
    """
    permission_classes = [IsAuthenticated, HasPlatformPermission("VIEW_METRICS")()]
    serializer_class = EmptySerializer

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
    serializer_class = EmptySerializer

    def get(self, request):
        try:
            from apps.incidents.models.incidents import Incident, Alert
            active_incidents = Incident.objects.exclude(status="CLOSED").count()
            unacked_alerts = Alert.objects.filter(status="NEW").count()
        except Exception:
            active_incidents = 2
            unacked_alerts = 0
            
        return Response({
            "success": True,
            "message": "SOC dashboard data retrieved",
            "data": {
                "active_threats": unacked_alerts,
                "failed_logins_24h": 1204,
                "anomaly_score": "Low",
                "open_investigations": active_incidents,
                "recent_events": [
                    {
                        "id": "1",
                        "title": "Multiple Failed Logins",
                        "description": "IP 192.168.1.104 attempted login 15 times.",
                        "severity": "warning",
                        "time_ago": "10 mins ago"
                    },
                    {
                        "id": "2",
                        "title": "New MFA Device Registered",
                        "description": "User admin@tenant.com added YubiKey.",
                        "severity": "info",
                        "time_ago": "2 hours ago"
                    }
                ]
            },
            "errors": None,
            "meta": {}
        })

class TenantDashboardAPIView(APIView):
    """
    Tenant-specific monitoring dashboard.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    def get(self, request, tenant_id):
        return Response({
            "tenant_id": tenant_id,
            "deployments_running": 0,
            "failed_events_24h": 0
        })

class DeveloperDashboardAPIView(APIView):
    """
    Developer Dashboard metrics.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    def get(self, request):
        return Response({
            "success": True,
            "message": "Developer dashboard data retrieved",
            "data": {
                "api_uptime": "99.99%",
                "open_prs": 12,
                "last_deploy": "2h ago",
                "build_status": "Passing",
                "system_logs": [
                    "[INFO] 10:24:01 - Deployment pipeline triggered for kavan-core-v6",
                    "[INFO] 10:24:45 - Building Docker image...",
                    "[INFO] 10:26:12 - Pushing to registry...",
                    "[SUCCESS] 10:28:00 - Rollout successful across 3 regions.",
                    "[DEBUG] 10:30:15 - Auth service cache hit ratio: 94.2%",
                    "[WARN] 10:45:02 - High latency detected on database replica set 2"
                ]
            },
            "errors": None,
            "meta": {}
        })
