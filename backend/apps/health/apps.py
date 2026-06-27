"""
KAVAN v6.0 — Health App Configuration
"""

from django.apps import AppConfig


class HealthConfig(AppConfig):
    """Health check application configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.health"
    label = "health"
    verbose_name = "Health"
