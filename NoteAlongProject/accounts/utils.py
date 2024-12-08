import logging
import time
from django.core.mail import send_mail
from django.conf import settings
from mailjet_rest import Client

logger = logging.getLogger(__name__)

def send_password_reset_email(user_email):
    subject = "Password Reset Successful"
    message = ("We would like to inform you that you have reset the password for your NoteAlong account.\n"
               "\nIf this was not done by you, please review your account as soon as possible!")
    retries = 3
    delay = 5  # seconds

    for i in range(retries):
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
            logger.info(f"Password reset email sent to {user_email}")
            break
        except Exception as e:
            logger.error(f"Failed to send email to {user_email}: {e}")
            if i < retries - 1:
                logger.info(f"Retrying... attempt {i + 2}")
                time.sleep(delay)
            else:
                logger.error(f"Max retries reached. Failed to send email to {user_email}.")



def send_welcome_email(user_email, username):
    mailjet = Client(auth=(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY), version='3.1')

    data = {
        'Message': [
            {
                'From': {
                    'Email': 'notealong@mail.com',
                    'Name': 'NoteAlong Team'
                },
                'To': [{
                    'Email': user_email,
                    'Name': username
                }],
                'Subject': 'Welcome to NoteAlong',
                'TextPart': 'We are happy to have you with us to enjoy the world of music!',

            }
        ]
    }
    result = mailjet.send.create(data=data)