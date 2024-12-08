from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model

from NoteAlongProject.accounts.models import Genre

UserModel = get_user_model()


class Concert(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    musician = models.ForeignKey(UserModel, related_name='concerts', on_delete=models.CASCADE)
    concertgoers = models.ManyToManyField(UserModel, blank=True, related_name='concertgoers')
    genres = models.ManyToManyField(Genre, blank=True, related_name='concerts')
    festival = models.ForeignKey('Festival', on_delete=models.CASCADE, related_name='concerts', null=True, blank=True)


    def save(self, *args, **kwargs):
        if self.musician and not getattr(self.musician.profile, 'is_musician', False):
            raise ValidationError(f"The user '{self.musician.username}' is not a musician.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Festival(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    genres = models.ManyToManyField(Genre, blank=True, related_name='festival_genres')


    def __str__(self):
        return self.title

