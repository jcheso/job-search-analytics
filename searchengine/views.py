from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def search_input(request):
    return HttpResponse("Search Engine")

def search_results(request):
    return HttpResponse("Search Results")    