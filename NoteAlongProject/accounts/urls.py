from django.urls import path, include

from NoteAlongProject.accounts.views import IndexView, SignupView, custom_logout, CustomLoginView

urlpatterns = [
    #    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
]