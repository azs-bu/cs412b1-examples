# blog/views.py
# define the views for the blog app
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from typing import Any

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView 
from .models import * ## import the models (e.g., Article)
from .forms import * ## import the forms (e.g., CreateCommentForm)
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth.models import User ## NEW
from django.contrib.auth import login ## NEW
import random

# class-based view
class ShowAllView(ListView):
    '''the view to show all Articles'''
    model = Article # the model to display
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' # context variable to use in the template

    def dispatch(self, *args, **kwargs):
        '''implement this method to add some debug tracing'''

        print(f"ShowAllView.dispatch; self.request.user={self.request.user}")
        # let the superclass version of this method do its work:
        return super().dispatch(*args, **kwargs)

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

class CreateCommentView(CreateView):
    '''
    A view to create a Comment on an Article.
    on GET: send back the form to display
    on POST: read/process the form, and save new Comment to the database
    '''

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        # get the context data from the sueprclass
        context =  super().get_context_data(**kwargs)

        # find the Article identified by the PK from the URL pattern
        article = Article.objects.get(pk=self.kwargs['pk'])
        
        # add the Article referred to by the URL into this context
        context['article'] = article
        return context

    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success.'''
        # return 'show_all' # a valid URL pattern
        # return reverse('show_all') # look up the URL called "show_all"

        # find the Article identified by the PK from the URL pattern
        article = Article.objects.get(pk=self.kwargs['pk'])
        return reverse('article', kwargs={'pk':article.pk})
        # return reverse('article', kwargs=self.kwargs)

    def form_valid(self, form):
        '''This method is called after the form is validated, 
        before saving data to the database.'''

        print(f'CreateCommentView.form_valid(): form={form.cleaned_data}')
        print(f'CreateCommentView.form_valid(): self.kwargs={self.kwargs}')

        # find the Article identified by the PK from the URL pattern
        article = Article.objects.get(pk=self.kwargs['pk'])

        # attach this Article to the instance of the Comment to set its FK
        form.instance.article = article # like: comment.article = article

        # delegate work to superclass version of this method
        return super().form_valid(form)


class CreateArticleView(LoginRequiredMixin, CreateView):
    '''A view class to create a new Article instance.'''

    form_class = CreateArticleForm
    template_name = 'blog/create_article_form.html'

    def get_login_url(self) -> str:
        '''return the URL of the login page'''
        return reverse('login')
    
    def form_valid(self, form):
        '''This method is called as part of the form processing.'''

        print(f'CreateArticleView.form_valid(): form.cleaned_data={form.cleaned_data}')

        # find the user who is logged in
        user = self.request.user

        # attach that user as a FK to the new Article instance
        form.instance.user = user

        # let the superclass do the real work
        return super().form_valid(form)

class RegistrationView(CreateView):
    '''Handle registration of new Users.'''

    template_name = 'blog/register.html' # we write this
    form_class = UserCreationForm # built-in from django.contrib.auth.forms

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        '''Handle the User creation form submission.'''
        
        # if we received an HTTP POST, we handle it 
        if self.request.POST:
            
            print(f"RegistrationView.dispatch: self.request.POST={self.request.POST}")
            
            # reconstruct the UserCreateForm from the POST data
            form = UserCreationForm(self.request.POST)

            if not form.is_valid():
                print(f"form.errors={form.errors}")

                # let CreateView.dispatch handle the problem
                return super().dispatch(request, *args, **kwargs)

            # save the form, which creates a new User
            user = form.save() # this will commit the insert to the database
            print(f"RegistrationView.dispatch: created user {user}.")

            # log the User in
            login(self.request, user)
            print(f"RegistrationView.dispatch: {user} is logged in.")

            # note for mini_fb: attach the FK user to the Profile form instance

            # return a response:
            return redirect(reverse('show_all'))


        # let CreateView.dispatch handle the HTTP GET request
        return super().dispatch(request, *args, **kwargs)