## formdata/urls.py
## define the URLs for this app

from django.urls import path
from django.conf import settings
from . import views

# define a list of valid URL patterns:
urlpatterns = [
    path(r'', views.show_form, name="show_form"), 
    path(r'submit', views.submit, name="submit"), ## new!
]
