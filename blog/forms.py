# blog/forms.py

from django import forms
from .models import Comment

class CreateCommentForm(forms.ModelForm):
    '''A form to add a COmment on an Article to the database'''

    class Meta:
        '''Associate this HTML form with the Comment data model'''
        model = Comment
        # fields = ['article', 'author', 'text'] # which fields to include in the form
        fields = ['author', 'text'] # which fields to include in the form]

