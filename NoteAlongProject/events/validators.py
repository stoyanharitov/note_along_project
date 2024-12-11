from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.timezone import now


@deconstructible
class DateValidator:
    def __init__(self, message=None):
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if value is None:
            self.__message = "The value cannot be before today's date"
        else:
            self.__message = value

    def __call__(self, value: str, *args, **kwargs):
        if value <= now():
            raise ValidationError(self.message)