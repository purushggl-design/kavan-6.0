from rest_framework.routers import DefaultRouter
from apps.monitoring.api.views import (
    EventViewSet, MetricViewSet, HealthCheckViewSet,
    PlatformDashboardAPIView, SOCDashboardAPIView, TenantDashboardAPIView,
    DeveloperDashboardAPIView
)

router = DefaultRouter()
router.register(r"events", EventViewSet, basename="events")
router.register(r"metrics", MetricViewSet, basename="metrics")
router.register(r"health-checks", HealthCheckViewSet, basename="health-checks")

from django.urls import path

urlpatterns = router.urls + [
    path("dashboards/platform/", PlatformDashboardAPIView.as_view(), name="platform-dashboard"),
    path("dashboards/soc/", SOCDashboardAPIView.as_view(), name="soc-dashboard"),
    path("dashboards/tenant/<uuid:tenant_id>/", TenantDashboardAPIView.as_view(), name="tenant-dashboard"),
    path("dashboards/developer/", DeveloperDashboardAPIView.as_view(), name="developer-dashboard"),
]
