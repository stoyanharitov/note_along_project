from rest_framework import serializers
from rest_framework.reverse import reverse_lazy

from .models import Post
from ..accounts.models import Genre


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    genres = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()
    genres_id = serializers.PrimaryKeyRelatedField(queryset= Genre.objects.all(), many=True, write_only=True)
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['pk', 'title', 'content', 'author', 'created_at', 'likes', 'genres', 'detail_url', 'genres_id']

    def get_author(self, obj):
        return obj.author.username if obj.author else None

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return reverse_lazy('post-api-detail', args=[obj.pk], request=request)

    def get_genres(self, obj):
        return [genre.name for genre in obj.genres.all()]

    def get_likes(self, obj):
        return [user.username for user in obj.likes.all()]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    detail_url = serializers.SerializerMethodField()
    liked_by = serializers.SerializerMethodField(read_only=True)
    post = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['pk', 'post', 'content', 'author', 'created_at', 'liked_by', 'detail_url']

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return reverse_lazy('comment-api-detail', args=[obj.pk], request=request)

    def get_liked_by(self, obj):
        return [user.username for user in obj.liked_by.all()]
