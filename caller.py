import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NoteAlongProject.settings')
django.setup()
#
# from NoteAlongProject.accounts.models import Genre
#
# genres = [
#     "Rock", "Pop", "Hip-Hop", "Jazz", "Classical", "Blues", "Electronic", "Reggae",
#     "Country", "Metal", "Funk", "Soul", "R&B", "Punk", "Disco", "Gospel",
#     "Techno", "House", "Trance", "Ska", "Folk", "Ambient", "Latin", "K-Pop",
#     "Indie", "Grunge", "Trap", "Dubstep", "Dancehall", "Afrobeats", "Synthwave",
#     "Industrial", "World", "Opera", "Chillout", "New Age", "Acoustic", "Swing",
#     "Bluegrass", "Hardcore", "Lo-fi"
# ]
#
#
# for genre_name in genres:
#     genre, created = Genre.objects.get_or_create(name=genre_name)
#     if created:
#         print(f"Added genre: {genre_name}")
#     else:
#         print(f"Genre already exists: {genre_name}")
#
# print("Done")

# def send_test_email():
#     send_mail(
#         'Test Email Subject',
#         'This is the email body.',
#         'stoyan@sto.yan',
#         ['cheapgin911@gmail.com'],
#         fail_silently=False,
#     )
#     print("Email sent successfully.")
#
# if __name__ == '__main__':
#     send_test_email()

# connection = get_connection(
#     backend='django.core.mail.backends.smtp.EmailBackend',
#     host='in-v3.mailjet.com',
#     port=587,
#     username='2d6988e6124fdcb5e8b890a42e043e32',
#     password='f3a24ab31470eaf3f92d70b72d6cf2c3',
#     use_tls=True
#     )

from django.core.mail import send_mail

send_mail(
    "Subject here",
    "Here is the message.",
    "note@along.com",
    ["stoyanharitov@gmail.com"],
    fail_silently=False,
)

print("Email sent successfully.")


# if __name__ == '__main__':
#     send_mail()