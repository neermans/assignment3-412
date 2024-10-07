# mini_fb/urls.py
# URL patterns for the mini_fb app 

from django.urls import path
from .views import ShowAllProfilesView

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
]