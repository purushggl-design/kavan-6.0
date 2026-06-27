"""
KAVAN v6.0 — Session Models
============================================================
Tracks active user sessions per device.

Session lifecycle:
  Created → Active → Expired | Revoked

Key rules:
  - Max 5 concurrent sessions per user (AuthConfig)
  - Inactivity timeout: 30 minutes
  - Absolute lifetime: 30 days
  - When limit exceeded, oldest session is auto-revoked

Sessions are soft-deleted (is_active=False), never hard-deleted,
to preserve the audit trail.

Note: Django's built-in Session model is NOT used here. KAVAN
sessions are JWT-bound, device-aware custom records.
"""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models.mixins import TimestampMixin


class Session(TimestampMixin):
    """
    JWT-backed user session.

    Tracks which device/IP/user-agent was used per login.
    Allows users to see and revoke their own active sessions
    from any device (like GitHub's "Sessions" page).

    The `session_token_hash` is the SHA-256 hash of a random
    session identifier stored in the JWT's `session_id` claim.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
        related_name="sessions",
        db_index=True,
        verbose_name=_("User"),
    )
    device_id = models.UUIDField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("Device ID"),
        help_text="References apps.devices.TrustedDevice.id if known.",
    )
    session_token_hash = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        verbose_name=_("Session Token Hash"),
        help_text="SHA-256 of the session identifier embedded in the JWT.",
    )

    # ---- Connection Metadata ----
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_("IP Address"),
    )
    user_agent = models.TextField(
        blank=True,
        verbose_name=_("User Agent"),
    )
    location = models.CharField(
        max_length=128,
        blank=True,
        verbose_name=_("Location"),
        help_text="Approximate geo location, e.g. 'Chennai, India'.",
    )

    # ---- Status ----
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name=_("Is Active"),
    )
    last_activity_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Last Activity At"),
        help_text="Updated on each authenticated request.",
    )
    expires_at = models.DateTimeField(
        verbose_name=_("Expires At"),
        help_text="Absolute expiry — 30 days from session creation.",
    )

    class Meta:
        db_table = "iam_sessions"
        verbose_name = _("Session")
        verbose_name_plural = _("Sessions")
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["user", "is_active"],
                name="idx_session_user_active",
            ),
            models.Index(fields=["expires_at"], name="idx_session_expires"),
            models.Index(
                fields=["last_activity_at"],
                name="idx_session_activity",
            ),
        ]

    def __str__(self) -> str:
        return (
            f"Session(user={self.user_id}, ip={self.ip_address}, "
            f"active={self.is_active})"
        )
