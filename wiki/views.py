from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

from .models import Article, ArticleCategory, Comment
from .forms import ArticleForm


class WikiListView(ListView):
    model = ArticleCategory
    template_name = 'wiki_articles.html'

class WikiDetailView(DetailView):
    model = Article, Comment
    template_name = 'wiki_details.html'
    redirect_field_name = '/wiki/articles'

class CreateWikiArticle(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'wiki_create.html'

    def get_success_url(self):
        return reverse_lazy('ledger:articles')