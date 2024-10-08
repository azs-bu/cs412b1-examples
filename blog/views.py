# blog/views.py
# define the views for the blog app
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import * ## import the models (e.g., Article)

import random

# class-based view
class ShowAllView(ListView):
    '''the view to show all Articles'''
    model = Article # the model to display
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' # context variable to use in the template

class RandomArticleView(DetailView):
    '''Display one Article selected at Random'''
    model = Article # the model to display
    template_name = "blog/article.html"
    context_object_name = "article"

    # AttributeError: Generic detail view RandomArticleView must be called with either an object pk or a slug in the URLconf.
    # one solution: implement get_object method
    def get_object(self):
        '''Return one Article chosed at random.'''

        # explicitly add an error to generate a call stack trace:
        # y = 3 / 0

        # retrieve all of the articles
        all_articles = Article.objects.all()
        # pick one at random
        article = random.choice(all_articles)
        return article

class ArticleView(DetailView):
    '''Display one Article selected by PK'''
    model = Article # the model to display
    template_name = "blog/article.html"
    context_object_name = "article"
