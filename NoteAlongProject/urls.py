from django.urls import path, include

urlpatterns = [
    #    path('admin/', admin.site.urls),
    path('', include('NoteAlongProject.accounts.urls')),
    path('posts/', include('NoteAlongProject.posts.urls')),
]
