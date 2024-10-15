# mini_fb/views.py

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile

class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

# New view to show individual profile
class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'
