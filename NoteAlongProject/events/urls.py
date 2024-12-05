from django.urls import path, include

from NoteAlongProject.events.views import ConcertCreateView, ConcertListView, ConcertEditView, ConcertDetailView, \
    concert_toggle_attendance

urlpatterns = [
    path('create-concert/', ConcertCreateView.as_view(), name='concert-create'),
    path('concerts/', include([
        path('', ConcertListView.as_view(), name='concert-list'),
        path('edit/<int:pk>/', ConcertEditView.as_view(), name='concert-edit'),
        path('details/<int:pk>/',
             include([path('', ConcertDetailView.as_view(), name='concert-details'),
                      path('toggle-attendance/', concert_toggle_attendance, name='concert-toggle-attendance'),
                      ]))
    ]))
    ]