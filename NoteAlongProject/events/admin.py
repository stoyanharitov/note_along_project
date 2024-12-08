from django.contrib import admin

from NoteAlongProject.events.models import Festival, Concert


@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'location',
                    'description',
                    'start_date',
                    'end_date',
                    'get_genres',
                    'get_concerts'
                    )
    search_fields = ('title', 'location', 'genres__name',)
    list_filter = ('title',)
    ordering = ('start_date',)

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])
    get_genres.short_description = 'Genres'

    def get_concerts(self, obj):
        return ", ".join([concert.title for concert in obj.concerts.all()])
    get_concerts.short_description = 'Concerts'


@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'location',
                    'description',
                    'musician',
                    'date',
                    'festival',
                    'get_genres',
                    'get_concertgoers',
                    )
    search_fields = ('title', 'location', 'genres__name', 'festival__title',)
    list_filter = ('title',)
    ordering = ('date',)

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])
    get_genres.short_description = 'Genres'

    def get_concertgoers(self, obj):
        return ", ".join([concertgoer.username for concertgoer in obj.concertgoers.all()])
    get_genres.short_description = 'Concertgoers'

