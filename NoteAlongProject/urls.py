from django.urls import path, include, re_path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.conf import settings
from NoteAlongProject.common.views import AboutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('reset-password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('', include('NoteAlongProject.accounts.urls')),
    path('posts/', include('NoteAlongProject.posts.urls')),
    path('events/', include('NoteAlongProject.events.urls')),
    path('search/', include('NoteAlongProject.common.urls')),
    path('about/', AboutView.as_view(), name='about'),
    ## Additional package directory
    path("select2/", include("django_select2.urls")),
]

if not settings.DEBUG:
    urlpatterns += [re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})]
