from django.contrib import admin
from NoteAlongProject.accounts.models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'city', 'age')
    search_fields = ('user__username', 'locacitytion')
    list_filter = ('age',)