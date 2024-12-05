from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('NoteAlongProject.accounts.urls')),
    path('posts/', include('NoteAlongProject.posts.urls')),
    path('events/', include('NoteAlongProject.events.urls')),
]
