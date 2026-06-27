"""KAVAN v6.0 — Devices App Configuration"""

from django.apps import AppConfig


class DevicesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.devices"
    label = "devices"
    verbose_name = "Trusted Devices"
