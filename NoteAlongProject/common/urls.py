from django.urls import path

from NoteAlongProject.common.views import search_results

urlpatterns = [
    path('', search_results, name='general-search'),
    ]