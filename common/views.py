from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Q
from NoteAlongProject.posts.models import Post
from NoteAlongProject.events.models import Concert, Festival
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

ModelUser = get_user_model()


class AboutView(TemplateView):
    template_name = 'about.html'


@login_required
def search_results(request):
    query = request.GET.get('query', '')
    category = request.GET.get('category', '')

    results = []

    if category == 'users':
        results = ModelUser.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(profile__music_genre_preferences__name__icontains=query)
        ).distinct()

    elif category == 'posts':
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query) |
            Q(genres__name__icontains=query)
        ).distinct().order_by('-created_at','title')

    elif category == 'concerts':
        results = Concert.objects.filter(
            (Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(musician__username__icontains=query) |
            Q(genres__name__icontains=query) |
            Q(location__icontains=query) |
            Q(festival__title__icontains=query)) &
            Q(date__gte=now())
        ).distinct().order_by('date', 'title')

    elif category == 'festivals':
        results = Festival.objects.filter(
            (Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(genres__name__icontains=query) |
            Q(concerts__title__icontains=query) |
            Q(concerts__title__icontains=query)) &
            Q(end_date__gte=now())

        ).distinct().order_by('-end_date','title')

    elif category == 'musicians':
        results = ModelUser.objects.filter(
            Q(profile__is_musician=True) &
            (Q(username__icontains=query) |
             Q(first_name__icontains=query) |
             Q(last_name__icontains=query) |
            Q(profile__music_genre_preferences__name__icontains=query))
        ).distinct().order_by('username')

    return render(request, 'common/general-search.html', {'results': results, 'query': query, 'category': category})