from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView, ListView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from .forms import SignupForm, ProfileForm
from NoteAlongProject.accounts.models import Profile
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect

from ..posts.models import Post


# Create your views here.
class  IndexView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """
        Filter the posts to show only those that have at least one genre in common
        with the user's preferred genres if logged in. Otherwise, return no posts.
        """
        if self.request.user.is_authenticated:
            # If user is authenticated, show posts based on their genres
            user_genres = self.request.user.profile.music_genre_preferences.all()
            return Post.objects.filter(genres__in=user_genres).distinct()
        else:
            # If user is not authenticated, return no posts
            return Post.objects.none()

    def get_context_data(self, **kwargs):
        # Add user login status to context
        context = super().get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        if self.request.user.is_authenticated:
            context['first_name'] = self.request.user.first_name
            context['last_name'] = self.request.user.last_name
        return context


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


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'account/profile-details.html'
    context_object_name = 'profile'

    def get_object(self):
        # Return the profile for the currently logged-in user
        return self.request.user.profile


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'account/profile-edit.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.profile

    def form_valid(self, form):
        form.save()
        return redirect('profile-details')