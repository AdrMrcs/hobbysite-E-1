from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Article, ArticleCategory


def index(request):
    return HttpResponse("hobby site")

class BlogListView(ListView):
    model = Article
    template_name = 'article_list.html'

class BlogDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'