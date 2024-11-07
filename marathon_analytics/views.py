from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Result

import plotly
import plotly.graph_objects as go

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
    
class ResultDetailView(DetailView):
    '''Display a single Result on it's own page.'''

    template_name = 'marathon_analytics/result_detail.html'
    model = Result
    context_object_name = "r"

    # implement some methods... 
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
        # get the superclass version of context
        context = super().get_context_data(**kwargs)
        r = context['r'] # obtain the single Result instance

        # get data: half-marathon splits
        first_half_seconds = (r.time_half1.hour * 3600 + 
                              r.time_half1.minute * 60 + 
                              r.time_half1.second)
        
        second_half_seconds = (r.time_half2.hour * 3600 + 
                              r.time_half2.minute * 60 + 
                              r.time_half2.second)
        
        # build a pie chart
        x = ['first half time', 'second half time']
        y = [first_half_seconds, second_half_seconds]
        # print(f'x={x}')
        # print(f'y={y}')
        fig = go.Pie(labels=x, values=y)
        pie_div = plotly.offline.plot({'data':[fig]},
                                      auto_open=False,
                                      output_type='div')
        
        # add the pie chart to the context
        context['pie_div'] = pie_div

        # create a bar chart with the number of runners passed and who passed by
        x = [f'runners passed by {r.first_name}',
             f'runner who passed {r.first_name}']
        y = [r.get_runners_passed(),
             r.get_runners_passed_by()]
        # print(f'x={x}')
        # print(f'y={y}')
        fig = go.Bar(x=x, y=y)
        bar_div = plotly.offline.plot({'data':[fig]},
                                      auto_open=False,
                                      output_type='div')
        # add this to the context data for use in the template
        context['bar_div'] = bar_div

        return context

