from django.urls import path, include

from NoteAlongProject.accounts.views import IndexView, SignupView, custom_logout, CustomLoginView, ProfileDetailView, \
    ProfileEditView, OtherUserProfileView, UserDeleteView, UserOwnPostsView, OtherUserProfilePostsView, \
    OtherUserProfileConcertsView, OtherUserFestivalsView

urlpatterns = [
    #    path('admin/', admin.site.urls),
    # User utilities views
    path('', IndexView.as_view(), name='index'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),

    # Accessing and CRUD for the current logged-in user
    path('profile/',
         include([
             path('', ProfileDetailView.as_view(), name='profile-details'),
             path('edit/', ProfileEditView.as_view(), name='profile-edit'),
             path('delete/', UserDeleteView.as_view(), name='profile-delete'),
             path('posts/', UserOwnPostsView.as_view(), name='profile-posts'),


             # Accessing another user's data
             path('<str:username>/', include([
                path('', OtherUserProfileView.as_view(), name='profile-other'),
                path('posts/', OtherUserProfilePostsView.as_view(), name='profile-posts-other'),
                path('concerts/', OtherUserProfileConcertsView.as_view(), name='profile-concerts-other'),
                path('festivals/', OtherUserFestivalsView.as_view(), name='profile-festivals-other'),]),

                  )


         ])),

]