from django.urls import path
from .views import DancerProfileListView, DancerProfileDetailView, CreateDancerProfileView

urlpatterns = [
    path('', DancerProfileListView.as_view(), name='dancer_profile_list'),
    path('dancer_profiles/<int:pk>/', DancerProfileDetailView.as_view(), name='dancer_profile_detail'),
    path('create_dancer_profile/', CreateDancerProfileView.as_view(), name='create_dancer_profile'),

]
