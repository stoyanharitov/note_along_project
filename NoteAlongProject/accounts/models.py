from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(to=UserModel, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    music_genre_preferences = models.ManyToManyField(to='Genre', blank=True)
    profile_pic = models.URLField(blank=True, null=True)
    is_musician = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        musician_group, created = Group.objects.get_or_create(name='Musician_admin')

        # Adding groups
        if self.is_musician:
            self.user.is_staff = True
            if musician_group not in self.user.groups.all():
                self.user.groups.add(musician_group)
        else:
            self.user.is_staff = False
            if musician_group in self.user.groups.all():
                self.user.groups.remove(musician_group)

        # Save the user and profile
        self.user.save()
        super(Profile, self).save(*args, **kwargs)



# need to create a custom migration for the genres in choices file
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name