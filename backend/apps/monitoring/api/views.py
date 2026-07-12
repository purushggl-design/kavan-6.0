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
        try:
            from apps.tenants.models import Tenant
            from apps.authentication.models import User
            from apps.audit.models import AuditEvent
            from apps.incidents.models.incidents import Incident, Alert

            tenant_count = Tenant.objects.count()
            user_count = User.objects.count()
            active_users = User.objects.filter(is_active=True).count()
            open_incidents = Incident.objects.exclude(status="CLOSED").count()
            
            # Fetch recent 3 audit logs
            recent_audit = []
            for event in AuditEvent.objects.order_by('-created_at')[:3]:
                recent_audit.append({
                    "actor": event.actor.email if event.actor else "System",
                    "event": event.action,
                    "desc": f"{event.module} - {event.status}",
                    "time": event.created_at.strftime("%Y-%m-%d %H:%M:%S")
                })

            # Data that does not have real models yet (Revenue, Subscriptions, Regional)
            # MUST be honestly reported as empty/0.
            return Response({
                "success": True,
                "message": "Platform metrics retrieved successfully",
                "data": {
                    "kpis": {
                        "total_tenants": tenant_count,
                        "total_users": user_count,
                        "active_users": active_users,
                        "monthly_revenue": 0,
                        "annual_forecast": 0,
                        "active_sessions": 0,
                        "api_requests": 0, # Could be wired to a real metric model later
                        "security_alerts": open_incidents
                    },
                    "charts": {
                        "monthly_revenue": [],
                        "user_growth": [],
                        "org_distribution": [],
                        "subscription_plans": [],
                        "api_monitoring_logs": [],
                        "security_analytics": [],
                        "tenant_growth": [],
                        "regional_data": []
                    },
                    "audit_timeline": recent_audit
                },
                "errors": None,
                "meta": {}
            })
        except Exception as e:
            return Response({
                "success": False,
                "message": "Failed to retrieve platform metrics",
                "data": None,
                "errors": str(e),
                "meta": {}
            }, status=500)

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
            active_incidents = 0
            unacked_alerts = 0
            
        return Response({
            "success": True,
            "message": "SOC dashboard data retrieved",
            "data": {
                "active_threats": unacked_alerts,
                "failed_logins_24h": 0, # Requires auth log model implementation
                "anomaly_score": "N/A", # Placeholder, requires real scoring logic
                "open_investigations": active_incidents,
                "recent_events": [] # Honest empty state
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
    Developer dashboard metrics.
    """
    permission_classes = [IsAuthenticated, HasPlatformPermission("VIEW_METRICS")()]
    serializer_class = EmptySerializer

    def get(self, request):
        return Response({
            "success": True,
            "message": "Developer dashboard data retrieved",
            "data": {
                "api_uptime": "N/A", # Requires metrics implementation
                "open_prs": 0, # Honest empty state
                "last_deploy": "N/A", # Requires deployment implementation
                "build_status": "N/A", # Requires CI implementation
                "system_logs": [] # Honest empty state
            },
            "errors": None,
            "meta": {}
        })
