"""
KAVAN v6.0 -- Authentication Signals
============================================================
Post-save signal: automatically creates UserProfile when a
new User record is created.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender='authentication.User')
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile automatically when a User is created."""
    if created:
        from apps.profiles.models import UserProfile
        UserProfile.objects.get_or_create(user=instance)
