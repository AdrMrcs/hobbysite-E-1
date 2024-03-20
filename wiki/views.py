from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Article


class WikiListView(ListView):
    model = Article
    template_name = 'wiki_articles.html'

class WikiDetailView(DetailView):
    model = Article
    template_name = 'wiki_details.html'
    redirect_field_name = '/wiki/articles'