"""
KAVAN v6.0 — Audit Models
============================================================
Immutable audit log for all security-relevant IAM events.

Design principles:
  - Records are NEVER updated or deleted (append-only)
  - Written asynchronously via AuditService (non-blocking)
  - Also written to the `kavan.audit` structured logger
  - Queryable by user, event type, IP, tenant, and date range

Event types are defined as constants in AuditEventType below.
Each event stores a structured JSON `metadata` field for
event-specific context (e.g. device info, failure reason).

Layer hooks:
  - tenant_id: populated for tenant-scoped events (Layer 3)
  - Future: SIEM export (Layer 7 — Security Suite)
"""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


# ============================================================
# AUDIT EVENT TYPE CONSTANTS
# ============================================================


class AuditEventType(models.TextChoices):
    """All auditable IAM events."""

    # Authentication
    LOGIN_SUCCESS         = "LOGIN_SUCCESS",          _("Login Success")
    LOGIN_FAILED          = "LOGIN_FAILED",           _("Login Failed")
    LOGOUT                = "LOGOUT",                 _("Logout")
    LOGOUT_ALL            = "LOGOUT_ALL",             _("Logout All Sessions")
    TOKEN_REFRESHED       = "TOKEN_REFRESHED",        _("Token Refreshed")
    TOKEN_REVOKED         = "TOKEN_REVOKED",          _("Token Revoked")

    # Account Security
    PASSWORD_CHANGED      = "PASSWORD_CHANGED",       _("Password Changed")
    PASSWORD_RESET_REQUESTED = "PASSWORD_RESET_REQUESTED", _("Password Reset Requested")
    PASSWORD_RESET_USED   = "PASSWORD_RESET_USED",    _("Password Reset Used")
    ACCOUNT_LOCKED        = "ACCOUNT_LOCKED",         _("Account Locked")
    ACCOUNT_UNLOCKED      = "ACCOUNT_UNLOCKED",       _("Account Unlocked")
    ACCOUNT_DISABLED      = "ACCOUNT_DISABLED",       _("Account Disabled")
    ACCOUNT_SUSPENDED     = "ACCOUNT_SUSPENDED",      _("Account Suspended")

    # Email Verification
    EMAIL_VERIFICATION_SENT   = "EMAIL_VERIFICATION_SENT",   _("Verification Email Sent")
    EMAIL_VERIFIED            = "EMAIL_VERIFIED",             _("Email Verified")

    # MFA
    MFA_ENABLED           = "MFA_ENABLED",            _("MFA Enabled")
    MFA_DISABLED          = "MFA_DISABLED",           _("MFA Disabled")
    MFA_VERIFIED          = "MFA_VERIFIED",           _("MFA Code Verified")
    MFA_FAILED            = "MFA_FAILED",             _("MFA Verification Failed")
    BACKUP_CODE_USED      = "BACKUP_CODE_USED",       _("Backup Code Used")
    BACKUP_CODES_REGENERATED = "BACKUP_CODES_REGENERATED", _("Backup Codes Regenerated")

    # Devices
    NEW_DEVICE_DETECTED   = "NEW_DEVICE_DETECTED",    _("New Device Detected")
    DEVICE_TRUSTED        = "DEVICE_TRUSTED",         _("Device Trusted")
    DEVICE_REMOVED        = "DEVICE_REMOVED",         _("Device Removed")

    # Sessions
    SESSION_CREATED       = "SESSION_CREATED",        _("Session Created")
    SESSION_EXPIRED       = "SESSION_EXPIRED",        _("Session Expired")
    SESSION_REVOKED       = "SESSION_REVOKED",        _("Session Revoked")

    # Profile
    PROFILE_UPDATED       = "PROFILE_UPDATED",        _("Profile Updated")

    # Service Accounts (Layer 8 stub)
    SERVICE_ACCOUNT_CREATED = "SERVICE_ACCOUNT_CREATED", _("Service Account Created")
    SERVICE_ACCOUNT_REVOKED = "SERVICE_ACCOUNT_REVOKED", _("Service Account Revoked")
    
    # Marketplace
    INSTALLATION_FAILED = "INSTALLATION_FAILED", _("Installation Failed")


# ============================================================
# AUDIT EVENT MODEL
# ============================================================


class AuditEvent(models.Model):
    """
    Immutable record of a security-relevant IAM event.

    Created via AuditService.log() — never directly.
    Fields are intentionally nullable so that events can be
    recorded even when partial information is available
    (e.g. failed login attempt by unknown user).

    NEVER add update() or delete() calls on this model.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    # ---- Who ----
    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_events",
        db_index=True,
        verbose_name=_("User"),
        help_text="Null for events where user is unknown (e.g. failed login).",
    )
    user_email = models.EmailField(
        blank=True,
        verbose_name=_("User Email (snapshot)"),
        help_text=(
            "Denormalized email stored at event time. "
            "Preserved even if user is later deleted."
        ),
    )

    # ---- What ----
    event_type = models.CharField(
        max_length=48,
        choices=AuditEventType.choices,
        db_index=True,
        verbose_name=_("Event Type"),
    )
    success = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name=_("Success"),
        help_text="False for failed attempts.",
    )
    failure_reason = models.CharField(
        max_length=128,
        blank=True,
        verbose_name=_("Failure Reason"),
        help_text="Short code for why the event failed, e.g. INVALID_PASSWORD.",
    )

    # ---- Where / Context ----
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_("IP Address"),
    )
    user_agent = models.TextField(
        blank=True,
        verbose_name=_("User Agent"),
    )
    device_id = models.UUIDField(
        null=True,
        blank=True,
        verbose_name=_("Device ID"),
    )
    location = models.CharField(
        max_length=128,
        blank=True,
        verbose_name=_("Location"),
        help_text="Approximate geo location.",
    )

    # ---- Structured Context ----
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Metadata"),
        help_text=(
            "Event-specific structured context. "
            "e.g. {session_id, device_name, failed_count}"
        ),
    )

    # ---- Layer 3 Hook ----
    tenant_id = models.UUIDField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("Tenant ID"),
        help_text="Populated by Layer 3 for tenant-scoped events.",
    )

    # ---- Timestamp (immutable) ----
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=_("Occurred At"),
    )

    class Meta:
        db_table = "iam_audit_events"
        verbose_name = _("Audit Event")
        verbose_name_plural = _("Audit Events")
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["user", "event_type"],
                name="idx_audit_user_event",
            ),
            models.Index(
                fields=["event_type", "created_at"],
                name="idx_audit_type_date",
            ),
            models.Index(
                fields=["ip_address", "created_at"],
                name="idx_audit_ip_date",
            ),
            models.Index(
                fields=["tenant_id", "created_at"],
                name="idx_audit_tenant_date",
            ),
        ]

    def __str__(self) -> str:
        return (
            f"AuditEvent({self.event_type}, user={self.user_email or 'anon'}, "
            f"success={self.success}, at={self.created_at})"
        )

    def save(self, *args, **kwargs):
        """Prevent updates to audit events (append-only)."""
        if not self._state.adding:
            raise PermissionError(
                "AuditEvent records are immutable and cannot be updated."
            )
        super().save(*args, **kwargs)
