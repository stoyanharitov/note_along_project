from django.urls import path, include
from rest_framework.routers import DefaultRouter

from NoteAlongProject.posts.views.post_views import PostViewSet, like_post, PostCreateView, PostEditView, \
    PostDetailView, PostDeleteView
from NoteAlongProject.posts.views.comment_views import CommentViewSet, add_comment, CommentDeleteView, like_comment, edit_comment

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post-api')
router.register(r'comments', CommentViewSet, basename='comment-api')

urlpatterns = [
    # Post REST endpoints
    path('api/', include(router.urls)),
    path('api/posts/<int:pk>/', PostViewSet.as_view({'get': 'list'}), name='post-api-detail'),
    path('api/comments/<int:pk>/', CommentViewSet.as_view({'get': 'list'}), name='comment-api-detail'),

    # Post and Comment functionality
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('like-post/', like_post, name='like-post'),
    path('<int:post_pk>/', include([
            path('edit/', PostEditView.as_view(), name='post-edit'),
            path('delete/', PostDeleteView.as_view(), name='post-delete'),
            path('add-comment/', add_comment, name='add-comment'),
            path('delete-comment/<int:comment_pk>/', CommentDeleteView.as_view(), name='delete-comment'),
            path('comments/<int:comment_pk>/like/', like_comment, name='like-comment'),
            path('comments/<int:comment_pk>/edit/', edit_comment, name='edit-comment'),
            path('', PostDetailView.as_view(), name='post-details'),]
    )),

]