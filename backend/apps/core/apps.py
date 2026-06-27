"""
KAVAN v6.0 — Core App Configuration
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Core application configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    label = "core"
    verbose_name = "Core"

    def ready(self):
        """Called when the app is ready. Run configuration checks."""
        from config.startup_checks import validate_configuration
        validate_configuration()

