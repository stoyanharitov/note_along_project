from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView, ListView, CreateView
from django.urls import reverse_lazy
from NoteAlongProject.accounts.forms import SignupForm, ProfileEditForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from NoteAlongProject.accounts.models import Profile
from NoteAlongProject.posts.models import Post
from NoteAlongProject.mixins import PaginationMixin

UserModel = get_user_model()


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

    # If already logged in
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')

        return super().dispatch(request, *args, **kwargs)


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


class UserDeleteView(LoginRequiredMixin, UpdateView):
    model = UserModel
    fields = []  # No fields to display in a form
    template_name = 'account/profile-delete.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        user = self.request.user
        if not user.is_authenticated:
            return HttpResponseForbidden("You are not authorized to perform this action.")

        return user

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        logout(self.request)

        return redirect(self.success_url)


class UserOwnPostsView(LoginRequiredMixin, PaginationMixin, ListView):
    model = Post
    template_name = 'common/profile-posts.html'
    context_object_name = 'posts'
    paginate_by = 5

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
