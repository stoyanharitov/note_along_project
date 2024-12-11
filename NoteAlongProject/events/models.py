from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import get_user_model

from NoteAlongProject.accounts.models import Genre
from NoteAlongProject.events.validators import DateValidator

UserModel = get_user_model()


class Concert(models.Model):
    title = models.CharField(max_length=50,
                             null = False,
                             blank = False,
                             unique = True,
                             validators =[MinLengthValidator(2)],
                             error_messages = {'unique': "Seems like the genre is already registered"},)
    date = models.DateTimeField(null = False,
                                blank = False,
                                validators = [DateValidator()],
                                )
    location = models.CharField(max_length=100,
                                null=False,
                                blank=False,
                                )
    description = models.TextField()
    musician = models.ForeignKey(UserModel, related_name='concerts', on_delete=models.CASCADE)
    concertgoers = models.ManyToManyField(UserModel, blank=True, related_name='concertgoers')
    genres = models.ManyToManyField(Genre, blank=False, related_name='concerts')
    festival = models.ForeignKey('Festival', on_delete=models.CASCADE, related_name='concerts', null=True, blank=True)


    def save(self, *args, **kwargs):
        if self.musician and not getattr(self.musician.profile, 'is_musician', False):
            raise ValidationError(f"The user '{self.musician.username}' is not a musician.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Festival(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateTimeField(null = False,
                                      blank = False,
                                      validators = [DateValidator()],
                                      )
    end_date = models.DateTimeField(null = False,
                                    blank = False,
                                    validators = [DateValidator()],
                                    )
    location = models.CharField(max_length=100,
                                null=False,
                                blank=False,
                                )
    description = models.TextField()
    genres = models.ManyToManyField(Genre, blank=False, related_name='festival_genres')


    def __str__(self):
        return self.title

