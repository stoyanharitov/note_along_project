from django.urls import path, include

from NoteAlongProject.posts.views import PostCreateView, like_post, PostEditView, PostDetailView, add_comment, \
    CommentDeleteView, like_comment, edit_comment

urlpatterns = [
    #    path('admin/', admin.site.urls),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('like-post/', like_post, name='like-post'),
    path('<int:post_pk>/', include([
            path('edit/', PostEditView.as_view(), name='post-edit'),
            path('add-comment/', add_comment, name='add-comment'),
            path('delete-comment/<int:comment_pk>/', CommentDeleteView.as_view(), name='delete-comment'),
            path('comments/<int:comment_pk>/like/', like_comment, name='like-comment'),
            path('comments/<int:comment_pk>/edit/', edit_comment, name='edit-comment'),
            path('', PostDetailView.as_view(), name='post-details'),

]
    )),

]