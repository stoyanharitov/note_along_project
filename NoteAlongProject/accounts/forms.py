from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from NoteAlongProject.accounts.models import Profile


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    # first I add fields for the first and last name
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'age', 'city', 'music_genre_preferences', 'profile_pic']
        widgets = {
            'music_genre_preferences': forms.CheckboxSelectMultiple(),
        }


    # getting the user model's first and last name and saving them alongside the other profile info
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = self.instance.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        if commit:
            profile.save()
        return profile
