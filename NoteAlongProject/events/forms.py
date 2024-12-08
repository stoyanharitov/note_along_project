from django import forms
from .models import Concert
from ..mixins import ReadOnlyMixin
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class ConcertForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = ['title', 'date', 'location', 'description','genres']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'genres': forms.CheckboxSelectMultiple(),
        }



class ConcertDeleteForm(ReadOnlyMixin, forms.ModelForm):
    read_only_fields = [ 'title', 'image_url', 'content']

    class Meta:
        model = Concert
        exclude = ('musician',)