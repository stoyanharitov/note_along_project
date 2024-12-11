import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NoteAlongProject.settings')
django.setup()

from NoteAlongProject.accounts.models import Genre

genres = [
    "Rock", "Pop", "Hip-Hop", "Jazz", "Classical", "Blues", "Electronic", "Reggae",
    "Country", "Metal", "Funk", "Soul", "R&B", "Punk", "Disco", "Gospel",
    "Techno", "House", "Trance", "Ska", "Folk", "Ambient", "Latin", "K-Pop",
    "Indie", "Grunge", "Trap", "Dubstep", "Dancehall", "Afrobeats", "Synthwave",
    "Industrial", "World", "Opera", "Chillout", "New Age", "Acoustic", "Swing",
    "Bluegrass", "Hardcore", "Lo-fi"
]

for genre_name in genres:
    genre, created = Genre.objects.get_or_create(name=genre_name)
    if created:
        print(f"Added genre: {genre_name}")
    else:
        print(f"Genre already exists: {genre_name}")

