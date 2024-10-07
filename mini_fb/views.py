# mini_fb/views.py
# define the views for the mini_fb app

from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView
from .models import Profile

class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'show_all_profiles.html'
    context_object_name = 'profiles'
