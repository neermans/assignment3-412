# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DancerProfile, DanceStyle, RecruiterProfile, PrivateMessage

class CreateDancerProfileForm(forms.ModelForm):
    class Meta:
        model = DancerProfile
        fields = ['name', 'bio', 'job_history', 'preferred_styles', 'image']

class CreateRecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = ['dance_company', 'email_contact', 'image']



class PrivateMessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your message here...'}),
        }