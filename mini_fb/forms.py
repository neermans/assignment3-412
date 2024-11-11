#mini_fb/forms.py

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'profile_image_url'] #collect all profile info

class CreateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['message']  # Collect the message

class UpdateProfileForm(forms.ModelForm):
     class Meta:
        model = Profile
        fields = ['city', 'email', 'profile_image_url']  # All fields that should not be changeable