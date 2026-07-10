"""
KAVAN v6.0 — Health App URL Configuration
"""

from django.urls import path

from apps.monitoring.health.views import (
    CeleryHealthView,
    DatabaseHealthView,
    HealthView,
    LivenessView,
    ReadinessView,
    RedisHealthView,
)
from apps.monitoring.health.system_view import SystemHealthView

app_name = "health"

urlpatterns = [
    path("", HealthView.as_view(), name="health"),
    path("live/", LivenessView.as_view(), name="liveness"),
    path("ready/", ReadinessView.as_view(), name="readiness"),
    path("db/", DatabaseHealthView.as_view(), name="database"),
    path("redis/", RedisHealthView.as_view(), name="redis"),
    path("celery/", CeleryHealthView.as_view(), name="celery"),
    path("system/", SystemHealthView.as_view(), name="system"),
]

