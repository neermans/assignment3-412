# voter_analytics/urls.py
from django.urls import path
from .views import VoterListView, VoterDetailView, GraphsView

urlpatterns = [
    path('', VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>', VoterDetailView.as_view(), name='voter'),  # Detail view for a single voter
    path('graphs', GraphsView.as_view(), name='graphs'), # view for the graphs

]
