from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets

from NoteAlongProject.posts.forms import CreatePostForm, PostEditForm
from NoteAlongProject.posts.models import Post, Comment
from NoteAlongProject.posts.permissions import IsPostAuthorOrSuperAdmin, IsCommentAuthorOrSuperAdmin
from NoteAlongProject.posts.serializers import PostSerializer, CommentSerializer


@login_required
def add_comment(request, post_pk):
    # Use 'id' instead of 'post_pk' as Post model's primary key
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(post=post, author=request.user, content=content)

    return redirect(reverse_lazy('post-details', kwargs={'post_pk': post_pk}))


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'posts/comment-delete.html'
    context_object_name = 'comment'
    pk_url_kwarg = 'comment_pk'

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        comment = get_object_or_404(Comment, pk=self.kwargs['comment_pk'], post=post)
        return comment

    def get_success_url(self):
        # Getting the post PK so that I can redirect
        post_pk = self.kwargs['post_pk']
        return reverse_lazy('post-details', kwargs={'post_pk': post_pk})


@login_required
def like_comment(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.user in comment.liked_by.all():
        comment.liked_by.remove(request.user)
        liked = False
    else:
        comment.liked_by.add(request.user)
        liked = True

    return JsonResponse({'liked': liked, 'total_likes': comment.liked_by.count()})


@login_required
def edit_comment(request, post_pk, comment_pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        comment = get_object_or_404(Comment, pk=comment_pk, post=post, author=request.user)

        data = json.loads(request.body)
        comment.content = data.get('content', comment.content)
        comment.save()
        return JsonResponse({'updated_content': comment.content}, status=200)

    return JsonResponse({'error': 'Invalid request'}, status=400)


# REST API views sets
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentAuthorOrSuperAdmin]

    def perform_create(self, serializer):
         pass

    def get_serializer_context(self):
         context = super().get_serializer_context()
         context['request'] = self.request
         return context