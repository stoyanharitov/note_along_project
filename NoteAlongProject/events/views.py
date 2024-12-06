from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.timezone import now

from NoteAlongProject.accounts.models import Profile
from NoteAlongProject.events.forms import ConcertForm, ConcertDeleteForm
from NoteAlongProject.events.models import Concert, Festival


class ConcertCreateView(LoginRequiredMixin, CreateView):
    model = Concert
    form_class = ConcertForm
    template_name = 'events/concert-create.html'
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.profile.is_musician:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.musician = self.request.user
        return super().form_valid(form)


class ConcertListView(LoginRequiredMixin, ListView):
    model = Concert
    template_name = 'common/profile-concerts.html'
    context_object_name = 'concerts'

    def get_queryset(self):
        user = self.request.user
        if user.profile.is_musician:
            return Concert.objects.filter(musician=user)
        else:
            return Concert.objects.filter(concertgoers=user)

    # def get(self, request, *args, **kwargs):
    #
    #     page_number = request.GET.get('page', 1)
    #
    #     queryset = self.get_queryset()
    #     paginator = Paginator(queryset, self.paginate_by)
    #
    #     try:
    #
    #         page_number = int(page_number)
    #         if page_number < 1:
    #             raise ValueError("Page number less than 1")
    #         elif page_number > paginator.num_pages:
    #             return HttpResponseRedirect(f'?page={paginator.num_pages}')
    #     except (ValueError, PageNotAnInteger):
    #         return HttpResponseRedirect('?page=1')
    #
    #     return super().get(request, *args, **kwargs)

class ConcertEditView(LoginRequiredMixin, UpdateView):
    model = Concert
    form_class = ConcertForm
    template_name = 'events/concert-edit.html'
    context_object_name = 'concert'

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

    def get_initial(self):
        return self.object.__dict__

    def form_invalid(self, form):
        return self.form_valid(form)


class ConcertsDashboardView(LoginRequiredMixin, ListView):
    model = Concert
    template_name = 'events/concert-dashboard.html'
    context_object_name = 'concerts'

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        user_genres = profile.music_genre_preferences.all()

        return Concert.objects.filter(genres__in=user_genres,
            date__gte=now()).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, user=self.request.user)

        context['profile'] = profile
        return context

class FestivalDashboardView(LoginRequiredMixin, ListView):
    model = Festival
    template_name = "events/festival-dashboard.html"
    context_object_name = "festivals"

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'profile') and user.profile.music_genre_preferences.exists():
            genres = user.profile.music_genre_preferences.all()
        else:
            genres = None


        queryset = Festival.objects.filter(
            end_date__gte=now()
        ).order_by("end_date")

        if genres:
            queryset = queryset.filter(genres__in=genres).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, user=self.request.user)

        context['profile'] = profile
        return context


class FestivalListView(LoginRequiredMixin, ListView):
    model = Festival
    template_name = "common/profile-festivals.html"
    context_object_name = "festivals"

    def get_queryset(self):
        user = self.request.user

        # Retrieve festivals that include concerts the user is a concertgoer of
        queryset = Festival.objects.filter(
            concerts__concertgoers=user
        ).distinct()  # Avoid duplicates if a festival has multiple matching concerts

        return queryset