from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NoteAlongProject.accounts'

class AccountsConfig(AppConfig):
    name = 'NoteAlongProject.accounts'

    def ready(self):
        import NoteAlongProject.accounts.signals