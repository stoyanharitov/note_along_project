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


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'posts/post-create.html'
    success_url = reverse_lazy('index')
    form_class = CreatePostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def like_post(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            # getting json body
            data = json.loads(request.body)
            post_id = data.get('post_id')  # from JSON

            # checking the post id
            if not post_id:
                return JsonResponse({'error': 'post_id is required'}, status=400)

            post = get_object_or_404(Post, id=post_id)

            if request.user in post.likes.all():
                post.likes.remove(request.user)
                liked = False
            else:
                post.likes.add(request.user)
                liked = True

            # getting updated likes
            total_likes = post.likes.count()

            post.save()
            return JsonResponse({'liked': liked, 'total_likes': total_likes})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = "posts/post-edit.html"
    pk_url_kwarg = 'post_pk'


    def get_success_url(self):
        previous_url = self.request.META.get('HTTP_REFERER')

        if previous_url and previous_url != self.request.build_absolute_uri():
            return previous_url
        else:
            post_pk = self.kwargs['post_pk']
            return reverse_lazy('post-details', kwargs={'post_pk': post_pk})


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post-details.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        return context


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
        # Getting the post pk so that I can redirect
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


# REST API view sets

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsPostAuthorOrSuperAdmin]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

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