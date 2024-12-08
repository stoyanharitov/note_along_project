from django.contrib import admin

# Register your models here.
from django.contrib import admin

from NoteAlongProject.posts.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','content','author','created_at',)
    list_filter = ('created_at','author__username',)
    ordering = ('created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post','content','author','created_at',)
    list_filter = ('created_at',)
    ordering = ('created_at',)