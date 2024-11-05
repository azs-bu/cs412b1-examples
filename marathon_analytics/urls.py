# marathon_analytics/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('', ResultsListView.as_view(), name="home"),
    path('results', ResultsListView.as_view(), name="results"),

]