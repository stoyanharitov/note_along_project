from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth import get_user_model
from django.db.models.signals import m2m_changed
from django.contrib.auth.models import User, Group
import threading

from .utils import send_welcome_email

UserModel = get_user_model()

# @receiver(post_save, sender=UserModel)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.get_or_create(user=instance)
#         send_welcome_email(instance.email, instance.username)
#
# @receiver(post_save, sender=UserModel)
# def save_user_profile(sender, instance, **kwargs):
#     if hasattr(instance, 'profile'):
#         instance.profile.save()


# @receiver(m2m_changed, sender=User.groups.through)
# def sync_profile_is_musician(sender, instance, action, pk_set, **kwargs):
#     if action in ['post_add', 'post_remove']:
#         musician_group = Group.objects.get(name='Musicians')
#         if musician_group.pk in pk_set:
#             instance.profile.is_musician = musician_group in instance.groups.all()
#             instance.profile.save()


@receiver(post_save, sender=Profile)
def update_user_staff_status(sender, instance, **kwargs):
    user = instance.user
    if instance.is_musician:
        user.is_staff = True
    else:
        user.is_staff = False
    print(user.username)
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



