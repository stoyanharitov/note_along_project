from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from NoteAlongProject.accounts.models import Profile


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Put your desired username here...'}),
            'email': forms.TextInput(attrs={'placeholder': 'Put your email address here...'}),
            'password1': forms.TextInput(attrs={'placeholder': 'Put your desired password here...'}),
            'password2': forms.TextInput(attrs={'placeholder': 'Repeat your password here...'}),
        }



class ProfileEditForm(forms.ModelForm):
    # First I add fields for the first and last name
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'age', 'city', 'music_genre_preferences', 'profile_pic']
        widgets = {
            'music_genre_preferences': forms.CheckboxSelectMultiple(),
            'first_name': forms.TextInput(attrs={'placeholder': 'Put your first name here...'}),
            'email': forms.TextInput(attrs={'placeholder': 'Put your email address here...'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Put your last name here...'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter your city here...'}),
        }


    # getting the user model's first and last name and saving them alongside the other profile info
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = self.instance.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        if commit:
            profile.save()
            self.save_m2m()
        return profile


