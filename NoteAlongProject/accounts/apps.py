from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NoteAlongProject.accounts'

    def ready(self):
        import NoteAlongProject.accounts.signals