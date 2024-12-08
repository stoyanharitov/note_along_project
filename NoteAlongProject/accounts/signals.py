from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth import get_user_model
from django.db.models.signals import m2m_changed
from django.contrib.auth.models import User, Group

from .utils import send_welcome_email

UserModel = get_user_model()

@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
        send_welcome_email(instance.email, instance.username)

@receiver(post_save, sender=UserModel)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


@receiver(m2m_changed, sender=User.groups.through)
def sync_profile_is_musician(sender, instance, action, pk_set, **kwargs):
    if action in ['post_add', 'post_remove']:
        musician_group = Group.objects.get(name='Musicians')
        if musician_group.pk in pk_set:
            instance.profile.is_musician = musician_group in instance.groups.all()
            instance.profile.save()


@receiver(post_save, sender=Profile)
def update_user_staff_status(sender, instance, **kwargs):
    user = instance.user
    if instance.is_musician:
        user.is_staff = True
    else:
        user.is_staff = False
    print(user.username)
    user.save()
