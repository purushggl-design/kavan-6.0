"""
KAVAN v6.0 — MFA Models
============================================================
Stores TOTP secrets and backup codes for multi-factor auth.

Security:
  - TOTP secret is NEVER stored in plain text.
    It is encrypted with Fernet (AES-256-CBC) using a key
    derived from settings.SECRET_KEY before storage.
  - Backup codes are stored as SHA-256 hashes (single-use).
  - One MFASecret per user; re-setup replaces the old record.

TOTP spec:
  - Algorithm: SHA1 (RFC 6238)
  - Digits:    6
  - Period:    30 seconds
  - Window:    ±1 step (handles minor clock drift)
"""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models.mixins import TimestampMixin


class MFASecret(TimestampMixin):
    """
    Stores the encrypted TOTP secret for a user.

    Lifecycle:
      1. User initiates MFA setup → record created (is_active=False)
      2. User scans QR code and submits a valid TOTP code
      3. is_active=True, User.mfa_enabled=True

    If the user re-enables MFA (after disable), the old record
    is replaced.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.OneToOneField(
        "authentication.User",
        on_delete=models.CASCADE,
        related_name="mfa_secret",
        verbose_name=_("User"),
    )
    secret_encrypted = models.TextField(
        verbose_name=_("Encrypted Secret"),
        help_text=(
            "Fernet-encrypted TOTP secret. "
            "Use MFAService.get_decrypted_secret() to read."
        ),
    )

    # TOTP parameters (stored for flexibility, currently always RFC 6238)
    algorithm = models.CharField(
        max_length=16,
        default="SHA1",
        verbose_name=_("Algorithm"),
    )
    digits = models.PositiveSmallIntegerField(
        default=6,
        verbose_name=_("Digits"),
    )
    period = models.PositiveSmallIntegerField(
        default=30,
        verbose_name=_("Period (seconds)"),
    )

    is_active = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name=_("Is Active"),
        help_text="False during setup phase. True after user verifies first TOTP code.",
    )
    verified_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Verified At"),
        help_text="Timestamp when user first verified the TOTP setup.",
    )

    class Meta:
        db_table = "iam_mfa_secrets"
        verbose_name = _("MFA Secret")
        verbose_name_plural = _("MFA Secrets")

    def __str__(self) -> str:
        return f"MFASecret(user={self.user_id}, active={self.is_active})"


class BackupCode(models.Model):
    """
    One-time backup codes for MFA recovery.

    Generated in batches of 10 (AuthConfig.MFA_BACKUP_CODES_COUNT).
    Each code is a 8-character alphanumeric string.
    Stored as SHA-256 hash — never in plain text.

    When the user regenerates backup codes, all existing unused
    codes are invalidated (is_used=True) before new ones are
    created.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
        related_name="backup_codes",
        db_index=True,
        verbose_name=_("User"),
    )
    code_hash = models.CharField(
        max_length=64,
        verbose_name=_("Code Hash"),
        help_text="SHA-256 hash of the plain backup code.",
    )
    is_used = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name=_("Is Used"),
        help_text="True once this code has been consumed for login.",
    )
    used_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Used At"),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "iam_backup_codes"
        verbose_name = _("Backup Code")
        verbose_name_plural = _("Backup Codes")
        ordering = ["created_at"]
        indexes = [
            models.Index(
                fields=["user", "is_used"],
                name="idx_bc_user_unused",
            ),
        ]

    def __str__(self) -> str:
        return f"BackupCode(user={self.user_id}, used={self.is_used})"
