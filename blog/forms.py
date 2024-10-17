# blog/forms.py

from django import forms
from .models import Comment, Article

class CreateCommentForm(forms.ModelForm):
    '''A form to add a Comment on an Article to the database'''

    class Meta:
        '''Associate this HTML form with the Comment data model'''
        model = Comment
        # fields = ['article', 'author', 'text'] # which fields to include in the form
        fields = ['author', 'text'] # which fields to include in the form]


class CreateArticleForm(forms.ModelForm):
    '''A form to add a new Article to the database.'''

    class Meta:
        '''Associate this HTML form with the Article data model.'''
        model = Article
        fields = ['author', 'title', 'text', 'image_file']