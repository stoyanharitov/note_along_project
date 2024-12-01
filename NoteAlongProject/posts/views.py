from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
import json

from NoteAlongProject.posts.forms import CreatePostForm, PostEditForm
from NoteAlongProject.posts.models import Post

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
    success_url = reverse_lazy('index')
    pk_url_kwarg = 'id'
    template_name = "posts/post-edit.html"