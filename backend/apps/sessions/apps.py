"""KAVAN v6.0 — IAM Sessions App Configuration"""

from django.apps import AppConfig


class SessionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.sessions"
    label = "iam_sessions"
    verbose_name = "IAM Sessions"
