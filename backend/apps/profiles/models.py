"""
KAVAN v6.0 — Profile Models
============================================================
Extended user preferences, notification settings, and
display information. Stored separately from the core User
model to keep the auth table lean.

One UserProfile per User (OneToOneField).
Created automatically via a post_save signal on User.
"""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models.mixins import TimestampMixin


class UserProfile(TimestampMixin):
    """
    Extended profile data for a KAVAN user.

    Includes:
      - Avatar URL
      - Bio and timezone
      - Notification preferences

    Automatically created when a User is created (signal in
    apps.authentication.signals).
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.OneToOneField(
        "authentication.User",
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name=_("User"),
    )

    # ---- Display ----
    avatar_url = models.URLField(
        blank=True,
        verbose_name=_("Avatar URL"),
        help_text="URL to the user's profile picture.",
    )
    bio = models.TextField(
        blank=True,
        max_length=500,
        verbose_name=_("Bio"),
    )

    # ---- Localisation ----
    timezone = models.CharField(
        max_length=64,
        default="UTC",
        verbose_name=_("Timezone"),
        help_text="IANA timezone identifier, e.g. 'Asia/Kolkata'.",
    )
    language = models.CharField(
        max_length=16,
        default="en",
        verbose_name=_("Language"),
        help_text="BCP 47 language tag, e.g. 'en', 'hi', 'ta'.",
    )
    date_format = models.CharField(
        max_length=32,
        default="YYYY-MM-DD",
        verbose_name=_("Date Format"),
        help_text="Preferred date display format.",
    )

    # ---- Notification Preferences ----
    email_notifications = models.BooleanField(
        default=True,
        verbose_name=_("Email Notifications"),
        help_text="Receive transactional emails (login alerts, etc.).",
    )
    push_notifications = models.BooleanField(
        default=True,
        verbose_name=_("Push Notifications"),
        help_text="Receive browser/mobile push notifications.",
    )
    marketing_emails = models.BooleanField(
        default=False,
        verbose_name=_("Marketing Emails"),
        help_text="Opt-in to product news and promotional content.",
    )

    class Meta:
        db_table = "iam_user_profiles"
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

    def __str__(self) -> str:
        return f"UserProfile({self.user.email})"
