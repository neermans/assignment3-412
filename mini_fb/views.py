# mini_fb/views.py

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .forms import *

class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

# New view to show individual profile
class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all status messages related to the profile
        context['status_messages'] = self.object.statusmessage_set.all()
        profile = self.get_object()
        for status in context['status_messages']:
            status.images = status.get_images()
        return context

#view to show the create a profile page
class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'
    
    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    
    


# view to show the create a new message page 
class CreateStatusMessageView(CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])  # Add the profile to the context
        return context

    def form_valid(self, form):
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile  # Attach the profile to the status message
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})  # Redirect to the profile page after submission