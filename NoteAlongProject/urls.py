from django.urls import path, include
from django.contrib import admin

from common.views import AboutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('NoteAlongProject.accounts.urls')),
    path('posts/', include('NoteAlongProject.posts.urls')),
    path('events/', include('NoteAlongProject.events.urls')),
    path('search/', include('common.urls')),
    path('about/', AboutView.as_view(), name='about'),
]
