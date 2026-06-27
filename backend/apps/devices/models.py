"""
KAVAN v6.0 — Devices Models
============================================================
Tracks devices used to access KAVAN.

Device fingerprinting:
  - User-Agent
  - Accept-Language header
  - IP address (as a soft signal)
  - Optional client-supplied fingerprint header

A device starts as is_trusted=False (new device detected).
It becomes trusted after the user acknowledges it (future:
email confirmation or explicit trust action).

This model drives:
  - New device login alerts
  - Session-to-device association
  - Trusted device bypass for MFA step-up (future)
"""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models.mixins import TimestampMixin


class DeviceType(models.TextChoices):
    DESKTOP = "DESKTOP", _("Desktop")
    MOBILE  = "MOBILE",  _("Mobile")
    TABLET  = "TABLET",  _("Tablet")
    CLI     = "CLI",     _("CLI / Script")
    SERVICE = "SERVICE", _("Service / API")
    UNKNOWN = "UNKNOWN", _("Unknown")


class TrustedDevice(TimestampMixin):
    """
    A physical or virtual device that has been used to log in.

    Device identity is determined by a computed fingerprint
    (hash of User-Agent + Accept-Language + optional client
    fingerprint). The same physical device will always
    produce the same fingerprint hash.

    Stores human-readable metadata (name, OS, browser) parsed
    from the User-Agent for display in the device management UI.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
        related_name="devices",
        db_index=True,
        verbose_name=_("User"),
    )

    # ---- Fingerprint ----
    device_fingerprint = models.CharField(
        max_length=64,
        db_index=True,
        verbose_name=_("Device Fingerprint"),
        help_text=(
            "SHA-256 of (user_agent + accept_language + optional_client_fp). "
            "Unique per user+device pair."
        ),
    )

    # ---- Display Info (parsed from User-Agent) ----
    device_name = models.CharField(
        max_length=128,
        blank=True,
        verbose_name=_("Device Name"),
        help_text="e.g. 'MacBook Pro', 'iPhone 15', 'Ubuntu Desktop'.",
    )
    device_type = models.CharField(
        max_length=16,
        choices=DeviceType.choices,
        default=DeviceType.UNKNOWN,
        verbose_name=_("Device Type"),
    )
    os = models.CharField(
        max_length=64,
        blank=True,
        verbose_name=_("Operating System"),
        help_text="e.g. 'macOS 14.1', 'Windows 11', 'Android 14'.",
    )
    browser = models.CharField(
        max_length=64,
        blank=True,
        verbose_name=_("Browser"),
        help_text="e.g. 'Chrome 126', 'Safari 17', 'Firefox 127'.",
    )

    # ---- Connection ----
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_("Last Known IP"),
    )

    # ---- Trust Status ----
    is_trusted = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name=_("Is Trusted"),
        help_text="Becomes True after user acknowledges the new device.",
    )
    last_seen_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Last Seen At"),
        help_text="Updated on every login from this device.",
    )

    class Meta:
        db_table = "iam_trusted_devices"
        verbose_name = _("Trusted Device")
        verbose_name_plural = _("Trusted Devices")
        ordering = ["-last_seen_at"]
        unique_together = [("user", "device_fingerprint")]
        indexes = [
            models.Index(
                fields=["user", "is_trusted"],
                name="idx_device_user_trusted",
            ),
            models.Index(
                fields=["device_fingerprint"],
                name="idx_device_fingerprint",
            ),
        ]

    def __str__(self) -> str:
        return (
            f"Device({self.user_id}, {self.device_name or 'Unknown'}, "
            f"trusted={self.is_trusted})"
        )
