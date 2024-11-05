from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from .models import Result

# Create your views here.
class ResultsListView(ListView):
    '''View to show a list of result.'''

    template_name = 'marathon_analytics/results.html'
    model = Result
    context_object_name = 'results'
    paginate_by = 50 # show 50 results per page

    def get_queryset(self) -> QuerySet[Any]:
        '''Limit the results to a small number of records'''

        # default query set is all of the records:
        qs = super().get_queryset()
        # return qs[:25] # limit to 25 records
        
        # handle search form/URL parameters:
        if 'city' in self.request.GET:

            city = self.request.GET['city']
            # filter the Results by this parameter
            qs = Result.objects.filter(city__icontains=city)

        return qs