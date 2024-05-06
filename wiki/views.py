from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

from .models import Article, ArticleCategory, Comment
from .forms import ArticleForm, CommentForms
from user_management import models as profilemodel

class LoginAuthenticator(object):
    def get_author_profile(self):
        if self.request.user.is_authenticated:
            author, _ = profilemodel.Profile.objects.get_or_create(user=self.request.user)
            return author
        return None

class WikiListView(LoginAuthenticator, ListView):
    model = ArticleCategory
    template_name = 'wiki_articles.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        author = self.get_author_profile()
        if author:
            authorArticles = Article.objects.filter(author=author)
            ctx['authorArticles'] = authorArticles
        return ctx

class WikiDetailView(LoginAuthenticator, DetailView):
    model = Article
    template_name = 'wiki_details.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        currentArticle = self.get_object()
        if self.request.user.is_authenticated:
            author = profilemodel.Profile.objects.get(user=self.request.user)
            articleFromAuthor = Article.objects.filter(author=author).exclude(pk=currentArticle.pk)
            ctx['articleFromAuthor'] = articleFromAuthor
            ctx['form'] = CommentForms()
            ctx['viewer'] = author
        return ctx
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForms(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = self.get_author_profile()
            comment.article = self.object
            comment.save()
            return redirect('wiki:article_details', pk=self.object.pk)
        else:
            ctx = self.get_context_data(form=form)
        return self.render_to_response(ctx)

class CreateWikiArticle(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'wiki_create.html'

    def get_success_url(self):
        return reverse_lazy('wiki:article_details', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        form.instance.author = profilemodel.Profile.objects.get(user=self.request.user)
        return super().form_valid(form)
    
class EditWikiArticle(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'wiki_edit.html'

    def get_success_url(self):
        return reverse_lazy('wiki:article_details', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)