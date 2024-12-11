from datetime import datetime
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse_lazy

from .models import Concert, Festival

UserModel = get_user_model()

class ConcertSerializer(serializers.ModelSerializer):
    musician = serializers.StringRelatedField(read_only=True)
    concertgoers = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all(), many=True, write_only=True)  # Editable by IDs in POST/PUT
    genres = serializers.SerializerMethodField()
    festival = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()
    concertgoer_usernames = serializers.SerializerMethodField()

    class Meta:
        model = Concert
        fields = ['pk', 'title', 'date', 'location', 'description', 'genres', 'festival', 'musician', 'concertgoers', 'concertgoer_usernames', 'detail_url']

    def get_genres(self, obj):
        return [genre.name for genre in obj.genres.all()]

    def get_festival(self, obj):
        return obj.festival.title if obj.festival else None

    def get_concertgoer_usernames(self, obj):
        return [concertgoer.username for concertgoer in obj.concertgoers.all()]

    def get_detail_url(self, obj):
        request = self.context.get('request')

        return reverse_lazy('concert-api-detail', args=[obj.pk], request=request)

    def validate_concertgoers(self, value):
        user = self.context['request'].user
        if user.id in [concertgoer.id for concertgoer in value]:
            raise ValidationError("You cannot add yourself as a concertgoer.")

        return value

    def validate_concertgoers(self, value):
        user = self.context['request'].user
        if user.id in [concertgoer.id for concertgoer in value]:
            raise ValidationError("You cannot add yourself as a concertgoer.")

        return value

    def validate_date(self, value):
        if value < timezone.now():
            raise ValidationError("The concert date cannot be in the past.")

        return value


class FestivalSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    concerts = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Festival
        fields = ('pk', 'title', 'start_date', 'end_date', 'location', 'description', 'genres', 'concerts', 'detail_url')

    def get_genres(self, obj):
        return [genre.name for genre in obj.genres.all()]

    def get_concerts(self, obj):
        return [concert.title for concert in obj.concerts.all()]

    def get_detail_url(self, obj):
        request = self.context.get('request')

        return reverse_lazy('festival-api-detail', args=[obj.pk], request=request)

    def validate_start_date(self, value):
        if value < timezone.now():
            raise ValidationError("The festival start date cannot be in the past.")

        end_date_str = self.initial_data.get('end_date')
        if end_date_str:
            try:
                # Convert the end date string to datetime
                end_date = timezone.make_aware(datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M"))
                if value >= end_date:
                    raise ValidationError("The festival start date must be before the end date.")
            except ValueError:
                raise ValidationError("The end date format is invalid.")

        return value