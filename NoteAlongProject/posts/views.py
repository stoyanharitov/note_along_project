from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CreatePostForm
from .models import Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'posts/post_create.html'
    success_url = reverse_lazy('index')
    form_class = CreatePostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)