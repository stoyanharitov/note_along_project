from django.views.generic import DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse, HttpResponseForbidden
import json
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets

from NoteAlongProject.posts.forms import CreatePostForm, PostEditForm, PostDeleteForm
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


@login_required()
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

            # Getting updated likes
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


    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        if post.author != self.request.user:
            return HttpResponseForbidden("You are not authorized to edit this post.")

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        previous_url = self.request.META.get('HTTP_REFERER')

        if previous_url and previous_url != self.request.build_absolute_uri():
            return previous_url
        else:
            post_pk = self.kwargs['post_pk']
            return reverse_lazy('post-details', kwargs={'post_pk': post_pk})


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/post-details.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()

        return context


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        if post.author != request.user:
            return HttpResponseForbidden("You are not authorized to delete this post.")
        form = PostDeleteForm(instance=post)

        return render(request, 'posts/post-delete.html', {'form': form, 'post': post})

    def post(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        if post.author != request.user:
            return HttpResponseForbidden("You are not authorized to delete this post.")
        post.delete()

        return redirect('index')  # Redirect to the list of posts or a relevant page


# REST API views sets
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