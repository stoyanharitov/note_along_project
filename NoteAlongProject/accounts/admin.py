from django.contrib import admin

# Register your models here.

from NoteAlongProject.accounts.models import Profile

# @admin.register(ModelUser)
# class ModelAdmin(admin.ModelAdmin):
#     list_display = ('username', 'first_name', 'last_name')  # Customize admin list view
#     search_fields = ('username',)  # Add a search bar
#     list_filter = ('username',)  # Add filtering options

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'city', 'age')
    search_fields = ('user__username', 'locacitytion')
    list_filter = ('age',)