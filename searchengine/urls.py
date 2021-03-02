from django.urls import path

from . import views

urlpatterns = [
    path('', views.search_input, name='search input'),
    path('results/', views.search_results, name='search results'),
]