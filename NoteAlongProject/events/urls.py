from django.urls import path, include
from rest_framework.routers import DefaultRouter

from NoteAlongProject.events.views.concert_views import ConcertViewSet, ConcertCreateView, UserConcertListView, \
    ConcertsDashboardView, ConcertEditView, ConcertDeleteView, ConcertDetailView, concert_toggle_attendance
from NoteAlongProject.events.views.festival_views import FestivalViewSet, UserFestivalListView, FestivalDashboardView, \
    FestivalDetailView

router = DefaultRouter()
router.register(r'concerts', ConcertViewSet, basename='concert-api')
router.register(r'festivals', FestivalViewSet, basename='festival-api')

urlpatterns = [
    # REST API endpoint
    path('api/', include(router.urls)),
    path('api/concerts/<int:pk>/', ConcertViewSet.as_view({'get': 'retrieve'}), name='concert-api-detail'),
    path('api/festivals/<int:pk>/', FestivalViewSet.as_view({'get': 'retrieve'}), name='festival-api-detail'),

    # Concert urls
    path('create-concert/', ConcertCreateView.as_view(), name='concert-create'),
    path('concerts/', include([
        path('', UserConcertListView.as_view(), name='concert-list'),
        path('dashboard/', ConcertsDashboardView.as_view(), name='concert-dashboard'),
        path('edit/<int:pk>/', ConcertEditView.as_view(), name='concert-edit'),
        path('delete/<int:pk>/', ConcertDeleteView.as_view(), name='concert-delete'),
        path('details/<int:pk>/',
             include([path('', ConcertDetailView.as_view(), name='concert-details'),
                      path('toggle-attendance/', concert_toggle_attendance, name='concert-toggle-attendance'),
                      ]))
    ])),


        # Festival urls
        path('festivals/', include([
            path('', UserFestivalListView.as_view(), name='festival-list'),
            path('dashboard/', FestivalDashboardView.as_view(), name='festival-dashboard'),
            path('details/<int:pk>', FestivalDetailView.as_view(), name='festival-details'),
        ])),
    ]