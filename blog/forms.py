#blog/forms.py

from django import forms
from .models import Comment


class CreateCommentForm(forms.ModelForm):
    '''a form to add a comment on an Article to the database '''

    class Meta:
        ''' associate this html form with the comment model'''
        model = Comment
        fields = ['author', 'text']