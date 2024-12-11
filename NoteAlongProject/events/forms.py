from django import forms
from .models import Concert, Genre
from django.contrib.auth import get_user_model
from django_select2.forms import ModelSelect2MultipleWidget
from ..mixins import ReadOnlyMixin

UserModel = get_user_model()


class ConcertCreateForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = ['title', 'date', 'location', 'description','genres']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'genres': forms.CheckboxSelectMultiple(),
            'title': forms.TextInput(attrs={'placeholder': 'Put your concert\'s title here...'}),
            'location': forms.TextInput(attrs={'placeholder': 'Put your concert\'s location here...'}),
            'description': forms.Textarea(attrs={'placeholder': 'Put a cool description for your concert here...'}),
        }



class ConcertDeleteForm(ReadOnlyMixin, forms.ModelForm):
    read_only_fields = [ 'title', 'image_url', 'content']

    class Meta:
        model = Concert
        exclude = ('musician',)