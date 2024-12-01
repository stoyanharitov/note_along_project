from django.urls import path, include

from NoteAlongProject.posts.views import PostCreateView, like_post, PostEditView

urlpatterns = [
    #    path('admin/', admin.site.urls),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('like-post/', like_post, name='like-post'),
    path('<int:id>/', include([
            path('edit/', PostEditView.as_view(), name='post-edit'),
]
    )),
]