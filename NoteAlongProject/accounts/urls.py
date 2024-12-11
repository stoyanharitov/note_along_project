from django.urls import path, include


from NoteAlongProject.accounts.views.auth_profile import SignupView, CustomLoginView, custom_logout, \
    ProfileDetailView, ProfileEditView, UserDeleteView, UserOwnPostsView
from NoteAlongProject.accounts.views.index_view import IndexView
from NoteAlongProject.accounts.views.other_user_profile import OtherUserProfileView, OtherUserProfilePostsView, \
    OtherUserConcertsView, OtherUserFestivalsView

urlpatterns = [
    # Index page with info from users
    path('', IndexView.as_view(), name='index'),

    # User auth utilities views
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
                path('concerts/', OtherUserConcertsView.as_view(), name='profile-concerts-other'),
                path('festivals/', OtherUserFestivalsView.as_view(), name='profile-festivals-other'),
                    ]),
                  )
         ])),
]