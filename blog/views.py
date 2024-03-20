from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Article, ArticleCategory


class BlogListView(ListView):
    model = ArticleCategory
    template_name = 'article_list.html'

class BlogDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'