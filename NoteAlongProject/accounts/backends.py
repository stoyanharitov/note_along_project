from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class EmailOrUsernameLoginBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        try:
            users = UserModel.objects.filter(email=username)
        except UserModel.DoesNotExist:
            return None

        for user in users:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None