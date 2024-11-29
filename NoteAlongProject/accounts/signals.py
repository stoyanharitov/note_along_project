from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth import get_user_model

UserModel = get_user_model()

@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=UserModel)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
