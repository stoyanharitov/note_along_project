from asgiref.sync import sync_to_async
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from .models import Concert
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Concert)
async def send_concert_creation_email(sender, instance, created, **kwargs):
    if created:
        user = await sync_to_async(lambda: instance.musician)()

        concert_title = instance.title
        concert_date = instance.date
        concert_location = instance.location

        subject = f"Thank you for registering your concert: {concert_title}"

        context = {
            'username': user.username,
            'concert_title': concert_title,
            'concert_date': concert_date,
            'concert_location': concert_location,
        }

        html_message = render_to_string('email/concert-creation-confirmation.html', context)
        plain_message = strip_tags(html_message)

        try:
            # Send the email asynchronously
            await sync_to_async(send_mail)(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message
            )
            logger.info(f"Concert creation email sent to {user.email} for concert '{concert_title}'.")
        except Exception as e:
            logger.error(f"Failed to send concert creation email to {user.email}: {e}")
