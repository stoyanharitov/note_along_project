from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from django.utils.timezone import now
from rest_framework.viewsets import ModelViewSet


from NoteAlongProject.accounts.models import Profile
from NoteAlongProject.events.models import Festival
from NoteAlongProject.events.permissions import IsSuperAdminOrReadOnly
from NoteAlongProject.events.serializers import FestivalSerializer
from NoteAlongProject.mixins import PaginationMixin


class FestivalDashboardView(LoginRequiredMixin, PaginationMixin, ListView):
    model = Festival
    template_name = 'events/festival-dashboard.html'
    context_object_name = 'festivals'
    paginate_by = 5

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        user_genres = profile.music_genre_preferences.all()

        return Festival.objects.filter(genres__in=user_genres,
            end_date__gte=now()).distinct().order_by('end_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, user=self.request.user)

        context['profile'] = profile
        return context


class UserFestivalListView(LoginRequiredMixin, PaginationMixin, ListView):
    model = Festival
    template_name = "common/profile-festivals.html"
    context_object_name = "festivals"
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user

        queryset = Festival.objects.filter(
            concerts__concertgoers=user,
            end_date__gte=now()
        ).distinct().order_by('end_date')

        return queryset


class FestivalDetailView(LoginRequiredMixin, DetailView):
    model = Festival
    template_name = 'events/festival-details.html'
    context_object_name = 'festival'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        festival = self.object

        concerts = festival.concerts.select_related('musician').prefetch_related('genres')
        context['concerts'] = concerts
        return context


# REST API views sets
class FestivalViewSet(ModelViewSet):
    queryset = Festival.objects.all()
    serializer_class = FestivalSerializer
    permission_classes = [IsSuperAdminOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request  # Add request context
        return context