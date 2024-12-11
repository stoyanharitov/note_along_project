from django.views.generic import ListView
from django.contrib.auth import get_user_model

from NoteAlongProject.posts.models import Post
from NoteAlongProject.mixins import PaginationMixin

UserModel = get_user_model()


class IndexView(PaginationMixin, ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user_genres = self.request.user.profile.music_genre_preferences.all()

            return (Post.objects.filter(genres__in=user_genres).
                    distinct().order_by('-created_at'))
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