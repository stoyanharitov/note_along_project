# Generated by Django 5.1.3 on 2024-12-11 16:54

from django.db import migrations


def populate_genres(apps, schema_editor):
    Genre = apps.get_model('accounts', 'Genre')

    # List of unique genre names
    genres = [
        "Rock", "Pop", "Jazz", "Classical", "Reggae",
        "Blues", "Country", "Hip Hop", "Electronic", "R&B",
        "Soul", "Funk", "Techno", "Latin", "Folk",
        "Disco", "Punk", "Metal", "Ska", "Indie"
    ]

    for genre_name in genres:
        Genre.objects.create(name=genre_name)

def reverse_genre_population(apps, schema_editor):
    Genre = apps.get_model('accounts', 'Genre')

    genres = [
        "Rock", "Pop", "Jazz", "Classical", "Reggae",
        "Blues", "Country", "Hip Hop", "Electronic", "R&B",
        "Soul", "Funk", "Techno", "Latin", "Folk",
        "Disco", "Punk", "Metal", "Ska", "Indie"
    ]
    Genre.objects.filter(name__in=genres).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0005_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.RunPython(populate_genres, reverse_genre_population),
    ]