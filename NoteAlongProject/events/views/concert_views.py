from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.utils.timezone import now
from rest_framework.viewsets import ModelViewSet


from NoteAlongProject.accounts.models import Profile
from NoteAlongProject.events.forms import ConcertCreateForm, ConcertDeleteForm
from NoteAlongProject.events.models import Concert, Festival
from NoteAlongProject.events.permissions import IsMusicianOwnerOrReadOnly, IsSuperAdminOrReadOnly
from NoteAlongProject.events.serializers import ConcertSerializer
from NoteAlongProject.mixins import PaginationMixin


class ConcertCreateView(LoginRequiredMixin, CreateView):
    model = Concert
    form_class = ConcertCreateForm
    template_name = 'events/concert-create.html'
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.profile.is_musician:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.musician = self.request.user
        return super().form_valid(form)


class UserConcertListView(LoginRequiredMixin, PaginationMixin, ListView):
    model = Concert
    template_name = 'common/profile-concerts.html'
    context_object_name = 'concerts'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        if user.profile.is_musician:
            return (Concert.objects.filter(musician=user, date__gte=now()).
                    distinct().order_by('date'))
        else:
            return (Concert.objects.filter(concertgoers=user, date__gte=now()).
                    distinct().order_by('date'))


class ConcertEditView(LoginRequiredMixin, UpdateView):
    model = Concert
    form_class = ConcertCreateForm
    template_name = 'events/concert-edit.html'
    context_object_name = 'concert'

    def dispatch(self, request, *args, **kwargs):
        concert = get_object_or_404(Concert, pk=self.kwargs['pk'])

        if concert.musician != self.request.user:
            return HttpResponseForbidden("You are not authorized to edit this concert.")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Concert.objects.filter(musician=self.request.user)

    def get_success_url(self):
        return reverse_lazy('concert-details', kwargs={'pk': self.object.pk})

class ConcertDetailView(LoginRequiredMixin, DetailView):
    model = Concert
    template_name = 'events/concert-details.html'
    context_object_name = 'concert'


@login_required
def concert_toggle_attendance(request, pk):
    if request.method == "POST":
        user = request.user
        concert = get_object_or_404(Concert, id=pk)

        if user == concert.musician:
            return JsonResponse({"error": "Creators cannot join their own concert."}, status=403)

        if user in concert.concertgoers.all():
            concert.concertgoers.remove(user)
            return JsonResponse({"attending": False})
        else:
            concert.concertgoers.add(user)
            return JsonResponse({"attending": True})

    return JsonResponse({"error": "Invalid request method."}, status=400)


class ConcertDeleteView(LoginRequiredMixin, DeleteView):
    model = Concert
    form_class = ConcertDeleteForm
    success_url = reverse_lazy('concert-list')
    template_name = 'events/concert-delete.html'

    def dispatch(self, request, *args, **kwargs):
        concert = get_object_or_404(Concert, pk=self.kwargs['pk'])

        if concert.musician != self.request.user:
            return HttpResponseForbidden("You are not authorized to delete this concert.")

        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return self.object.__dict__

    def form_invalid(self, form):
        return self.form_valid(form)


class ConcertsDashboardView(LoginRequiredMixin, PaginationMixin, ListView):
    model = Concert
    template_name = 'events/concert-dashboard.html'
    context_object_name = 'concerts'
    paginate_by = 5

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        user_genres = profile.music_genre_preferences.all()

        return Concert.objects.filter(genres__in=user_genres,
            date__gte=now()).distinct().order_by('date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, user=self.request.user)

        context['profile'] = profile
        return context


# REST API views sets
class ConcertViewSet(ModelViewSet):
    queryset = Concert.objects.all()
    serializer_class = ConcertSerializer
    permission_classes = [IsMusicianOwnerOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(musician=self.request.user)