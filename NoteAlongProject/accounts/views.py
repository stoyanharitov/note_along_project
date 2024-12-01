from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView, ListView, TemplateView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from .forms import SignupForm, ProfileEditForm
from NoteAlongProject.accounts.models import Profile
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


from ..posts.models import Post

ModelUser = get_user_model()

class  IndexView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user_genres = self.request.user.profile.music_genre_preferences.all()
            return Post.objects.filter(genres__in=user_genres).distinct()
        else:
            return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        if self.request.user.is_authenticated:
            context['first_name'] = self.request.user.first_name
            context['last_name'] = self.request.user.last_name
            context['username'] = self.request.user.username
        return context


class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'account/signup.html'
    success_url = reverse_lazy('login')

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
        return self.request.user.profile


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'account/profile-edit.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.profile

    def form_valid(self, form):
        form.save()
        return redirect('profile-details')


class OtherUserProfileView(TemplateView):
    template_name = 'account/profile-other.html'

    def dispatch(self, request, *args, **kwargs):
        username = self.kwargs.get('username')

        # Check if the logged-in user matches the username
        if request.user.is_authenticated and request.user.username == username:
            return self.redirect_to_owner_profile()

        # Fetch profile details for another user
        user = get_object_or_404(User, username=username)
        self.profile = get_object_or_404(Profile, user=user)
        return super().dispatch(request, *args, **kwargs)

    def redirect_to_owner_profile(self):
        return redirect(reverse_lazy('profile-details'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile
        context['first_name'] = self.profile.user.first_name
        context['last_name'] = self.profile.user.last_name
        return context