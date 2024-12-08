from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NoteAlongProject.events'

    def ready(self):
        import NoteAlongProject.events.signals

# class EConfig(AppConfig):
#     name = 'NoteAlongProject.events'

