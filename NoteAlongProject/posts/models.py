from django.db import models
from django.contrib.auth import get_user_model

from NoteAlongProject.accounts.models import Genre

UserModel = get_user_model()

class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name="Post Title")
    content = models.TextField(verbose_name="Post Content")
    author = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name="posts")
    likes = models.ManyToManyField(to=UserModel, related_name="liked_posts", blank=True)
    genres = models.ManyToManyField(to=Genre, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(verbose_name="Comment Content")
    created_at = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(to=UserModel, related_name='liked_comments', blank=True)

    def __str__(self):
        return self.author.username

    @property
    def total_comment_likes(self):
        return self.liked_by.count()
