from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView, ListView, TemplateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignupForm, ProfileEditForm
from NoteAlongProject.accounts.models import Profile
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger
from django.http import HttpResponseRedirect

from ..posts.models import Post

ModelUser = get_user_model()

class  IndexView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    paginate_by = 5

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
                raise ValueError("Page number less than 1")
            elif page_number > paginator.num_pages:
                # Redirect to the last page if the number is too high
                return HttpResponseRedirect(f'?page={paginator.num_pages}')
        except (ValueError, PageNotAnInteger):
            # Redirect to the first page if the number is invalid
            return HttpResponseRedirect('?page=1')

        # Call the parent class's get method to continue
        return super().get(request, *args, **kwargs)


class SignupView(CreateView):
    model = ModelUser
    form_class = SignupForm
    template_name = 'account/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        return response


class CustomLoginView(LoginView):
    template_name = 'account/login.html'


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

        # Check if the logged-in user matches the username
        if request.user.is_authenticated and request.user.username == username:
            return self.redirect_to_owner_profile()

        # Get profile details for another user
        user = get_object_or_404(ModelUser, username=username)
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
    model = ModelUser
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
            return Post.objects.filter(author__exact=self.request.user)
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
                raise ValueError("Page number less than 1")
            elif page_number > paginator.num_pages:
                # Redirect to the last page if the number is too high
                return HttpResponseRedirect(f'?page={paginator.num_pages}')
        except (ValueError, PageNotAnInteger):
            # Redirect to the first page if the number is invalid
            return HttpResponseRedirect('?page=1')

        # Call the parent class's get method to continue
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
        # Check if the logged-in user matches the username
        if request.user.is_authenticated and request.user.username == username:
            return self.redirect_to_owner_profile_posts()

        # Get profile details for another user
        user = get_object_or_404(ModelUser, username=username)
        self.profile = get_object_or_404(Profile, user=user)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Post.objects.filter(author=self.profile.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        if self.request.user.is_authenticated:
            context['first_name'] = self.profile.user.first_name
            context['last_name'] = self.profile.user.last_name
            context['profile_username'] = self.profile.user.username
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
                raise ValueError("Page number less than 1")
            elif page_number > paginator.num_pages:
                # Redirect to the last page if the number is too high
                return HttpResponseRedirect(f'?page={paginator.num_pages}')
        except (ValueError, PageNotAnInteger):
            # Redirect to the first page if the number is invalid
            return HttpResponseRedirect('?page=1')

        # Call the parent class's get method to continue
        return super().get(request, *args, **kwargs)


