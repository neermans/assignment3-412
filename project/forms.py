# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DancerProfile, DanceStyle, RecruiterProfile

class CreateDancerProfileForm(forms.ModelForm):
    class Meta:
        model = DancerProfile
        fields = ['name', 'bio', 'job_history', 'preferred_styles']

    def __init__(self, *args, **kwargs):
        super(CreateDancerProfileForm, self).__init__(*args, **kwargs)
        self.fields['preferred_styles'].queryset = DanceStyle.objects.all()


class CreateRecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = ['dance_company', 'email_contact']
