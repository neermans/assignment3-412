# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

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

class DancePostForm(forms.ModelForm):
    class Meta:
        model = DancePost
        fields = ['video', 'cut_music', 'description']

class CommentBoardPostForm(forms.ModelForm):
    class Meta:
        model = CommentBoardPost
        fields = ['content', 'post_type']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']