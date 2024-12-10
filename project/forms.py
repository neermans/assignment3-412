# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

# form to create a dancer profile
class CreateDancerProfileForm(forms.ModelForm):
    class Meta:
        model = DancerProfile
        fields = ['name', 'bio', 'job_history', 'preferred_styles', 'image']

# form to create a recruiter profile
class CreateRecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = ['dance_company', 'email_contact', 'image']

# form to create a private message between two profiles
class PrivateMessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your message here...'}),
        }

# form to create a dance post, either a video or a piece of cut music
class DancePostForm(forms.ModelForm):
    class Meta:
        model = DancePost
        fields = ['video', 'cut_music', 'description']

# form to create a comment post, can be one of three types
class CommentBoardPostForm(forms.ModelForm):
    class Meta:
        model = CommentBoardPost
        fields = ['content', 'post_type']

# form to create a comment on a post of someones
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']