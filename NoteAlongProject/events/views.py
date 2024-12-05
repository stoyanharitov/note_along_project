from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.core.paginator import Paginator, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from NoteAlongProject.events.forms import ConcertForm
from NoteAlongProject.events.models import Concert


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
    template_name = 'events/profile-concerts.html'
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


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Concert

@login_required
def concert_toggle_attendance(request, pk):
    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    concert = get_object_or_404(Concert, pk=pk)

    # Toggle the user's attendance status
    if request.user in concert.concertgoers.all():
        concert.concertgoers.remove(request.user)
        attending = False
    else:
        concert.concertgoers.add(request.user)
        attending = True

    # Return a JSON response indicating the updated attendance status
    return JsonResponse({
        'attending': attending,
        'user': {
            'username': request.user.username,
            'id': request.user.id,  # Include user ID to locate the list item
        }
    })