# marathon_analytics/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('', ResultsListView.as_view(), name="home"),
    path(r'results', ResultsListView.as_view(), name="results"),
    path(r'result/<int:pk>', ResultDetailView.as_view(), name="result_detail"), ## NEW


]