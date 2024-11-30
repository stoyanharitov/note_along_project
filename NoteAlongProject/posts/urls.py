from django.urls import path

from NoteAlongProject.posts.views import PostCreateView

urlpatterns = [
    #    path('admin/', admin.site.urls),
    path('create/', PostCreateView.as_view(), name='post-create'),
    ]