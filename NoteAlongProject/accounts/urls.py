from django.urls import path, include

from NoteAlongProject.accounts.views import IndexView, SignupView, custom_logout, CustomLoginView, ProfileDetailView, \
    ProfileEditView

urlpatterns = [
    #    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('profile/',
         include([
             path('', ProfileDetailView.as_view(), name='profile-details'),
             path('edit/', ProfileEditView.as_view(), name='profile-edit'),
         ])),

]