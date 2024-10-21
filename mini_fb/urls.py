# mini_fb/urls.py
# URL patterns for the mini_fb app 

from django.urls import path
from . import views
from .views import ShowAllProfilesView, ShowProfilePageView, CreateProfileView, CreateStatusMessageView, UpdateProfileView, DeleteStatusMessageView, UpdateStatusMessageView

urlpatterns = [
    path('', views.ShowAllProfilesView.as_view(), name='show_all_profiles'), #to show all the profiles
    path('profile/<int:pk>/', views.ShowProfilePageView.as_view(), name='show_profile'), #to show specific profiles
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'), #to create a new profile
    path('profile/<int:pk>/create_status/', CreateStatusMessageView.as_view(), name='create_status'),  # New URL for status messages
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name='update_profile'), # New URL for updating profile
    path('profile/status/<int:pk>/delete', views.DeleteStatusMessageView.as_view(), name='delete_status'), # New URL for deleting a status message
    path('profile/status/<int:pk>/update', views.UpdateStatusMessageView.as_view(), name='update_status'), # New URL for updating a status message
]
