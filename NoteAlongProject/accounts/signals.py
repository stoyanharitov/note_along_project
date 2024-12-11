from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
import threading

UserModel = get_user_model()


@receiver(post_save, sender=Profile)
def update_user_staff_status(sender, instance, **kwargs):
    user = instance.user
    if instance.is_musician or user.is_superuser:
        user.is_staff = True
    else:
        user.is_staff = False

    user.save()


# Schedule deletion
# Dictionary to keep track of active timers
active_timers = {}

def schedule_deletion(user_id, delay_seconds):
    def delete_user():
        try:
            user = User.objects.get(id=user_id)
            if not user.is_active:
                user.delete()
        except User.DoesNotExist:
            pass

    timer = threading.Timer(delay_seconds, delete_user)
    active_timers[user_id] = timer
    timer.start()

def cancel_deletion(user_id):
    timer = active_timers.get(user_id)
    if timer:
        timer.cancel()
        del active_timers[user_id]

@receiver(post_save, sender=User)
def handle_user_activation(sender, instance, **kwargs):
    """Handles user activation and deactivation."""
    if instance.is_active:
        # If the user is reactivated, cancel any scheduled deletion
        cancel_deletion(instance.id)
    else:
        # Schedule deletion for deactivated users
        delay_seconds = 30 * 24 * 60 * 60  # 30 days in seconds
        schedule_deletion(instance.id, delay_seconds)
        print(f"Deactivation timer started for user {instance.username}")



