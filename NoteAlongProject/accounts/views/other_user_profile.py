from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from NoteAlongProject.events.models import Concert, Festival
from NoteAlongProject.accounts.models import Profile
from NoteAlongProject.posts.models import Post
from NoteAlongProject.mixins import PaginationMixin

UserModel = get_user_model()


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


class OtherUserProfilePostsView(LoginRequiredMixin, PaginationMixin, ListView):
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
        return (Post.objects.filter(author=self.profile.user)
                .order_by('-created_at'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated

        if self.request.user.is_authenticated:
            context['first_name'] = self.profile.user.first_name
            context['last_name'] = self.profile.user.last_name
            context['profile_username'] = self.profile.user.username

        return context


class OtherUserConcertsView(LoginRequiredMixin, PaginationMixin, ListView):
    model = Concert
    template_name = 'common/profile-concerts-other.html'
    context_object_name = 'concerts'
    paginate_by = 5


    def get_queryset(self):
        profile_user = get_object_or_404(UserModel, username=self.kwargs.get('username'))

        if profile_user.profile.is_musician:
            queryset = Concert.objects.filter(musician=profile_user,
                                                  date__gte=now()).distinct().order_by('date')
        else:
            queryset = Concert.objects.filter(concertgoers=profile_user,
                                                   date__gte=now()).distinct().order_by('date')

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile_user = get_object_or_404(UserModel, username=self.kwargs.get('username'))
        context['profile_user'] = profile_user

        return context


class OtherUserFestivalsView(LoginRequiredMixin, PaginationMixin, ListView):
    model = Festival
    template_name = ('common/profile-festivals-other.html')
    context_object_name = 'festivals'
    paginate_by = 5

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