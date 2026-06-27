"""
KAVAN v6.0 — Accounts Models: Password History
============================================================
Stores hashed previous passwords to enforce the no-reuse
policy (last N passwords cannot be reused, configured in
AuthConfig.PASSWORD_HISTORY_LIMIT).

Kept in a separate `accounts` app to follow SRP — password
lifecycle management is distinct from core authentication.
"""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class PasswordHistory(models.Model):
    """
    Stores Argon2 hashes of previous passwords.

    Used by PasswordService.check_password_history() to
    prevent reuse of the last N passwords.

    Records are NEVER deleted (audit trail); they simply age
    out of the reuse-window after PASSWORD_HISTORY_LIMIT newer
    entries exist.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
        related_name="password_history",
        db_index=True,
        verbose_name=_("User"),
    )
    password_hash = models.CharField(
        max_length=256,
        verbose_name=_("Password Hash"),
        help_text="Argon2 hash of the old password.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Changed At"),
        help_text="Timestamp when this password was set.",
    )

    class Meta:
        db_table = "iam_password_history"
        verbose_name = _("Password History")
        verbose_name_plural = _("Password History")
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["user", "created_at"],
                name="idx_ph_user_created",
            ),
        ]

    def __str__(self) -> str:
        return f"PasswordHistory(user={self.user_id}, at={self.created_at})"
