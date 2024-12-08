from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView, ListView, TemplateView, DeleteView, CreateView
from django.urls import reverse_lazy
from .forms import SignupForm, ProfileEditForm
from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.utils.timezone import now
import threading
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator

from NoteAlongProject.events.models import Concert, Festival
from NoteAlongProject.accounts.models import Profile
from NoteAlongProject.posts.models import Post
from NoteAlongProject.accounts.utils import send_password_reset_email

UserModel = get_user_model()

class  IndexView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user_genres = self.request.user.profile.music_genre_preferences.all()
            return Post.objects.filter(genres__in=user_genres).distinct().order_by('created_at')
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

    def get(self, request, *args, **kwargs):
        # Get the page number from query parameters
        page_number = request.GET.get('page', 1)

        # Fetch the queryset
        queryset = self.get_queryset()

        # Initialize the paginator
        paginator = Paginator(queryset, self.paginate_by)

        try:
            # Validate the page number
            page_number = int(page_number)
            if page_number < 1:
                raise ValueError('Page number less than 1')
            elif page_number > paginator.num_pages:
                # Redirect to the last page if the number is too high
                return HttpResponseRedirect(f'?page={paginator.num_pages}')
        except (ValueError, PageNotAnInteger):
            # Redirect to the first page if the number is invalid
            return HttpResponseRedirect('?page=1')

        # Call the parent class's get method to continue
        return super().get(request, *args, **kwargs)


class SignupView(CreateView):
    model = UserModel
    form_class = SignupForm
    template_name = 'account/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        return response


class CustomLoginView(LoginView):
    template_name = 'account/login.html'

    def form_valid(self, form):
        user = form.get_user()
        if not hasattr(user, 'profile'):
            Profile.objects.get_or_create(user=user)
        return super().form_valid(form)


@login_required
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


class OtherUserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile-other.html'

    def redirect_to_owner_profile(self):
        return redirect(reverse_lazy('profile-details'))

    def dispatch(self, request, *args, **kwargs):
        username = self.kwargs.get('username')

        if request.user.is_authenticated and request.user.username == username:
            return self.redirect_to_owner_profile()

        user = get_object_or_404(UserModel, username=username)
        self.profile = get_object_or_404(Profile, user=user)
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile
        context['first_name'] = self.profile.user.first_name
        context['last_name'] = self.profile.user.last_name
        context['username'] = self.profile.user.username
        return context


class UserDeleteView(LoginRequiredMixin,  DeleteView):
    model = UserModel
    template_name = 'account/profile-delete.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        print(f"User attempting to delete: {self.request.user.username}")
        return self.request.user

    def delete(self, request, *args, **kwargs):
        self.get_object().profile.delete()
        return super().delete(request, *args, **kwargs)


class UserOwnPostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'common/profile-posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(author__exact=self.request.user).order_by('created_at')
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

    def get(self, request, *args, **kwargs):
        page_number = request.GET.get('page', 1)

        queryset = self.get_queryset()

        paginator = Paginator(queryset, self.paginate_by)

        try:
            page_number = int(page_number)
            if page_number < 1:
                raise ValueError('Page number less than 1')
            elif page_number > paginator.num_pages:
                return HttpResponseRedirect(f'?page={paginator.num_pages}')
        except (ValueError, PageNotAnInteger):
            return HttpResponseRedirect('?page=1')

        return super().get(request, *args, **kwargs)


class OtherUserProfilePostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'common/profile-posts-other.html'
    context_object_name = 'posts'
    paginate_by = 5

    def redirect_to_owner_profile_posts(self):
        return redirect(reverse_lazy('profile-posts'))

    def dispatch(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        if request.user.is_authenticated and request.user.username == username:
            return self.redirect_to_owner_profile_posts()

        user = get_object_or_404(UserModel, username=username)
        self.profile = get_object_or_404(Profile, user=user)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Post.objects.filter(author=self.profile.user).order_by('created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        if self.request.user.is_authenticated:
            context['first_name'] = self.profile.user.first_name
            context['last_name'] = self.profile.user.last_name
            context['profile_username'] = self.profile.user.username
        return context

    def get(self, request, *args, **kwargs):

        page_number = request.GET.get('page', 1)

        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)

        try:

            page_number = int(page_number)
            if page_number < 1:
                raise ValueError('Page number less than 1')
            elif page_number > paginator.num_pages:
                return HttpResponseRedirect(f'?page={paginator.num_pages}')
        except (ValueError, PageNotAnInteger):
            return HttpResponseRedirect('?page=1')

        return super().get(request, *args, **kwargs)


class OtherUserProfileConcertsView(LoginRequiredMixin, ListView):
    model = Concert
    template_name = 'common/profile-concerts-other.html'
    context_object_name = 'concerts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile_user = get_object_or_404(UserModel, username=self.kwargs['username'])

        concertgoer_concerts = Concert.objects.filter(concertgoers=profile_user,
                                                      date__gte=now()).distinct().order_by('date')

        created_concerts = Concert.objects.filter(musician=profile_user,
                                                  date__gte=now()).distinct().order_by('date')

        # Add both to the context
        context['profile_user'] = profile_user
        context['concertgoer_concerts'] = concertgoer_concerts
        context['created_concerts'] = created_concerts

        return context


class OtherUserFestivalsView(LoginRequiredMixin, ListView):
    model = Festival
    template_name = ('common/profile-festivals-other.html')
    context_object_name = 'festivals'

    def get_queryset(self):
        profile_user = self.kwargs.get('username')

        queryset = Festival.objects.filter(
            concerts__concertgoers__username=profile_user,
            end_date__gte=now()
        ).distinct().order_by('end_date')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = self.get_profile_user()
        return context

    def get_profile_user(self):
        username = self.kwargs.get('username')
        return get_object_or_404(UserModel, username=username)


