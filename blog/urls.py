## blog/urls.py
## description: URL patterns for the blog app

from django.urls import path
from django.conf import settings
from . import views

# all of the URLs that are part of this app
urlpatterns = [
    path(r'', views.ShowAllView.as_view(), name="show_all"),
    # path(r'about', views.about, name="about"),
    
]