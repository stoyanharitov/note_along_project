from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    music_genre_preferences = models.ManyToManyField(to='Genre', blank=True)
    profile_pic = models.URLField(blank=True, null=True)



# need to create a custom migration for the genres in choices file
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name