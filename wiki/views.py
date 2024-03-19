from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Articles
# Create your views here.

def index(request):
    return HttpResponse('index')

class WikiListView(ListView):
    model = Articles
    template_name = 'wiki_articles.html'

class WikiDetailView(DetailView):
    model = Articles
    template_name = 'wiki_details.html'
    redirect_field_name = '/wiki/articles'