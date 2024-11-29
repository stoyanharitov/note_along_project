from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from .forms import SignupForm
from NoteAlongProject.accounts.models import Profile
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect

# Create your views here.
class  IndexView(TemplateView):
    template_name = 'index.html'


class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'account/signup.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        return response


class CustomLoginView(LoginView):
    template_name = 'account/login.html'

def custom_logout(request):
    logout(request)
    return redirect(reverse_lazy('index'))