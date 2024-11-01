# mini_fb/urls.py
# URL patterns for the mini_fb app 

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import ShowAllProfilesView, ShowProfilePageView, CreateProfileView, CreateStatusMessageView, UpdateProfileView, DeleteStatusMessageView, UpdateStatusMessageView, CreateFriendView, ShowFriendSuggestionsView, ShowNewsFeedView

urlpatterns = [
    path('', views.ShowAllProfilesView.as_view(), name='show_all_profiles'), #to show all the profiles
    path('profile/<int:pk>/', views.ShowProfilePageView.as_view(), name='show_profile'), #to show specific profiles
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'), #to create a new profile
    path('profile/<int:pk>/create_status/', CreateStatusMessageView.as_view(), name='create_status'),  # New URL for status messages
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name='update_profile'), # New URL for updating profile
    path('profile/status/<int:pk>/delete', views.DeleteStatusMessageView.as_view(), name='delete_status'), # New URL for deleting a status message
    path('profile/status/<int:pk>/update', views.UpdateStatusMessageView.as_view(), name='update_status'), # New URL for updating a status message
    path('profile/<int:pk>/add_friend/<int:other_pk>', CreateFriendView.as_view(), name='add_friend'), # New URL for creating a friend 
    path('profile/<int:pk>/friend_suggestions', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'), # New URL for showing friend suggestions for a user
    path('profile/<int:pk>/news_feed', ShowNewsFeedView.as_view(), name='news_feed'), # New URL for showing the news feed of a profile
    path('login/', auth_views.LoginView.as_view(template_name = 'mini_fb/login.html'), name='login'),  # New URL for login
    path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name='logout'), # New URL for logout page
    

]
