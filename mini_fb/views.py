# mini_fb/views.py

from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin # assignment 9, redirects users to login page if not authenticated
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


# View to see all the profiles
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
    
    # find and return the profile associated with this user to find the page
    def get_object(self):
        return get_object_or_404(Profile, pk=self.kwargs['pk'])

#view to show the create a profile page, can do logged in or not logged in
class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success'''
        return reverse('show_profile', kwargs={'pk': self.object.pk})  # Directly use self.object.pk
    
    def get_context_data(self, **kwargs):
        '''Return the context from the user form'''
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        '''Return the new user if the user form is submitted in a valid form'''
        user_form = UserCreationForm(self.request.POST)

        if user_form.is_valid():
            new_user = user_form.save()
            form.instance.user = new_user
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, user_form=user_form))
        


# view to show the create a new message page, must be logged in to do 
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        '''Return the context from the profile'''
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, user=self.request.user) # Add the profile to the context
        return context

    def form_valid(self, form):
        '''Checks if the form is falid, if yes, saves the status message to the profile'''
        profile =get_object_or_404(Profile, user=self.request.user)
        form.instance.profile = profile  # Attach the profile to the status message
        sm = form.save()

        #saves the files if there were any submitted
        files = self.request.FILES.getlist('files')  # Retrieve list of uploaded files
        if files:
            for f in files:
                image = Image(image=f, status_message=sm)
                image.save()
            print(f"Image uploaded: {image.image.url}")
        else:
            print("No images uploaded")
        
        return super().form_valid(form)

    def get_success_url(self):
        '''Return the URL to redirect to on success'''
        return reverse('show_profile', kwargs={'pk': self.request.user.profile.pk})  # Redirect to the profile page after submission
  

#view to update the profile selected, must be logged in to update your profile
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self):
        '''Return the URL to redirect to on success'''
        return reverse('show_profile', kwargs={'pk': self.request.user.profile.pk})  # Redirect to the profile page after submission
    
    # make sure only logged in users can update a profile
    def get_login_url(self) -> str:
        '''return the URL of the login page'''
        return reverse('login')
    
    # find and return the profile associated with this user to find the page
    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)
    
    
#view to delete a status message, must be logged in
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status'

    def get_success_url(self):
        '''Return the URL to redirect to on success'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk}) # Redirect to the profile page after submission
    
    def get_login_url(self) -> str:
        '''return the URL of the login page'''
        return reverse('login')
    
#view to update the status message , must be logged in
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    model = StatusMessage
    fields = ['message']  
    template_name = 'mini_fb/update_status_form.html'

    def get_success_url(self):
        '''Return the URL to redirect to on success'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk}) # Redirect to the profile page after submission
    
    def get_login_url(self) -> str:
        '''return the URL of the login page'''
        return reverse('login')
    
# view to create a new friend, must be logged in
class CreateFriendView(LoginRequiredMixin, CreateView):
    def dispatch(self, request, *args, **kwargs):
        other_pk = kwargs.get('other_pk')
        
        # Retrieve the profiles
        profile = get_object_or_404(Profile, user=self.request.user)
        other_profile = get_object_or_404(Profile, pk=other_pk)
        
        # Check if trying to add oneself as a friend
        if profile == other_profile:
            return redirect('show_profile', pk=profile.pk)  # Redirect back to the profile page if self-adding

        # Add friend
        profile.add_friend(other_profile)
        
        # Redirect to the profile page
        return redirect('show_profile', pk=profile.pk)
    
    def get_login_url(self) -> str:
        '''return the URL of the login page'''
        return reverse('login')
    
# view to show friend suggestions of people the user is not already friends with, must be logged in to see profiles friend suggestions
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        # gets the data of the friend suggestions
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['suggestions'] = profile.get_friend_suggestions()
        return context
    
    def get_login_url(self) -> str:
        '''return the URL of the login page'''
        return reverse('login')
    
    # find and return the profile associated with this user to find the page
    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)
    

# view to show the actual news feed, must be logged in to see profiles news feed
class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        '''gets and returns the context data of the news feed of the profile'''
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['news_feed'] = profile.get_news_feed()  # Use the get_news_feed method
        return context
    
    def get_login_url(self) -> str:
        '''return the URL of the login page'''
        return reverse('login')
    
    # find and return the profile associated with this user to find the page
    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)