from django.http import HttpResponse
from django.template import loader
import time
import sys

from .models import SearchInput
from . import main


def search_input(request):
    context = {}
    template = loader.get_template('searchengine/index.html')
    return HttpResponse(template.render(context, request))


def search_results(request):
    if request.method == 'GET':  # If the form is submitted
        job_search = request.GET.get('job_search', None)
        location_search = request.GET.get('location_search', None)

    number_of_jobs, average_pay_min, average_pay_max, most_frequent_location, top_companies, currency, top_words, job, location = main.get_analytics(
        job_search, location_search)
    context = {
        'number_of_jobs': number_of_jobs,
        'job_search': job,
        'location_search': location,
        'average_pay_min': average_pay_min,
        'average_pay_max': average_pay_max,
        'most_frequent_location': most_frequent_location,
        'top_companies': top_companies[0:20],
        'currency': currency,
        'top_words': top_words[0:20]
    }

    template = loader.get_template('searchengine/results.html')
    return HttpResponse(template.render(context, request))
