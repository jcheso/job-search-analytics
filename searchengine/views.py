from django.http import HttpResponse
from django.template import loader

from .models import SearchInput
from . import main

def search_input(request):
    context = {}
    template = loader.get_template('searchengine/index.html')
    return HttpResponse(template.render(context, request))

def search_results(request):
    if request.method == 'GET': # If the form is submitted
        job_search = request.GET.get('job_search', None)
        location_search = request.GET.get('location_search', None)

    average_pay, most_frequent_location, count_companies, currency = main.get_analytics(job_search,location_search)
    context = { 
        'job_search': job_search,
        'location_search': location_search,
        'average_pay': average_pay,
        'most_frequent_location': most_frequent_location,
        'count_companies': count_companies,
        'currency': currency
    }
    template = loader.get_template('searchengine/results.html')
    return HttpResponse(template.render(context, request))

  