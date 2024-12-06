from django.urls import path, include

from NoteAlongProject.events.views import ConcertCreateView, ConcertListView, ConcertEditView, ConcertDetailView, \
    concert_toggle_attendance, ConcertDeleteView, ConcertsDashboardView, FestivalDashboardView, FestivalListView

urlpatterns = [
    path('create-concert/', ConcertCreateView.as_view(), name='concert-create'),
    path('concerts/', include([
        path('', ConcertListView.as_view(), name='concert-list'),
        path('dashboard/', ConcertsDashboardView.as_view(), name='concert-dashboard'),
        path('edit/<int:pk>/', ConcertEditView.as_view(), name='concert-edit'),
        path('delete/<int:pk>/', ConcertDeleteView.as_view(), name='concert-delete'),
        path('details/<int:pk>/',
             include([path('', ConcertDetailView.as_view(), name='concert-details'),
                      path('toggle-attendance/', concert_toggle_attendance, name='concert-toggle-attendance'),
                      ]))
    ])),
        path('festivals/', include([
            path('',FestivalDashboardView.as_view(), name='festival-dashboard'),
            path('festivals/',FestivalListView.as_view(), name='festival-list'),
        ])),
    ]