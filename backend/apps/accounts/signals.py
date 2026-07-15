from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from apps.accounts.models import PasswordHistory

User = get_user_model()

@receiver(pre_save, sender=User)
def track_password_history(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = User.objects.get(pk=instance.pk)
            if old_instance.password != instance.password:
                # Save the old password hash to history
                PasswordHistory.objects.create(
                    user=instance,
                    password_hash=old_instance.password
                )
        except User.DoesNotExist:
            pass
