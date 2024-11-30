from django.db import models
from django.contrib.auth import get_user_model

from NoteAlongProject.accounts.models import Genre

ModelUser = get_user_model()

class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name="Post Title")
    content = models.TextField(verbose_name="Post Content")
    author = models.ForeignKey(to=ModelUser, on_delete=models.CASCADE, related_name="posts")
    likes = models.ManyToManyField(to=ModelUser, related_name="liked_posts", blank=True)
    genres = models.ManyToManyField(to=Genre, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(to=ModelUser, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(verbose_name="Comment Content")
    created_at = models.DateTimeField(auto_now_add=True)

