# mini_fb/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin # assignment 9, redirects users to login page if not authenticated

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

#view to show the create a profile page
class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'
    def form_valid(self, form):
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')

        username = f"{first_name}{last_name}".lower()

        original_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{original_username}{counter}"
            counter += 1

        new_user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name)

        form.instance.user = new_user
        return super().form_valid(form)
        

    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success'''
        return reverse('show_profile', kwargs={'pk': self.object.pk})  # Directly use self.object.pk



# view to show the create a new message page 
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, user=self.request.user) # Add the profile to the context
        return context

    def form_valid(self, form):
        profile =get_object_or_404(Profile, user=self.request.user)
        form.instance.profile = profile  # Attach the profile to the status message
        sm = form.save()

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
        return reverse('show_profile', kwargs={'pk': self.request.user.profile.pk})  # Redirect to the profile page after submission
  

#view to update the profile selected
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.request.user.profile.pk})  # Redirect to the profile page after submission
    
    # make sure only logged in users can update a profile
    def get_login_url(self) -> str:
        '''return the URL of the login page'''
        return reverse('login')
    
    # find and return the profile associated with this user to find the page
    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)
    
    
#view to delete a status message
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk}) # Redirect to the profile page after submission
    
    def get_login_url(self) -> str:
        '''return the URL of the login page'''
        return reverse('login')
    
#view to update the status message 
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    model = StatusMessage
    fields = ['message']  
    template_name = 'mini_fb/update_status_form.html'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk}) # Redirect to the profile page after submission
    
    def get_login_url(self) -> str:
        '''return the URL of the login page'''
        return reverse('login')
    
# view to create a new friend 
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
    
# view to show friend suggestions of people the user is not already friends with
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
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
    

# view to show the actual news feed  
class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
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