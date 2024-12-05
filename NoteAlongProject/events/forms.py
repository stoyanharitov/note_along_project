from django import forms
from .models import Concert

class ConcertForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = ['title', 'date', 'location', 'description','genres']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'genres': forms.CheckboxSelectMultiple(),
        }