from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import Group

class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    music_genre_preferences = models.ManyToManyField(to='Genre', blank=True)
    profile_pic = models.URLField(blank=True, null=True)
    is_musician = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Automatically add user to groups based on role
        musician_group, _ = Group.objects.get_or_create(name='Musicians')
        normal_user_group, _ = Group.objects.get_or_create(name='Normal Users')

        if self.is_musician:
            self.user.groups.add(musician_group)
            self.user.groups.remove(normal_user_group)
        else:
            self.user.groups.add(normal_user_group)
            self.user.groups.remove(musician_group)



# need to create a custom migration for the genres in choices file
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name