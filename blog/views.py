from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy

from .models import Article, ArticleCategory
from user_management import models as profilemodel
from .forms import CommentForms, ArticleForms


class LoginAuthenticator(object):
    def get_author_profile(self):
        if self.request.user.is_authenticated:
            author, _ = profilemodel.Profile.objects.get_or_create(user=self.request.user)
            return author
        return None

class BlogListView(LoginAuthenticator, ListView):
    model = ArticleCategory
    template_name = 'article_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        author = self.get_author_profile()
        if author:
            ownarticles = Article.objects.filter(author=author)
            ctx['ownarticles'] = ownarticles
        return ctx

class BlogDetailView(LoginAuthenticator, DetailView):
    model = Article
    template_name = 'article_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        article = self.get_object()
        if self.request.user.is_authenticated:
            author = profilemodel.Profile.objects.get(user=self.request.user)
            ownarticles = Article.objects.filter(author=author)
            ctx['ownarticles'] = ownarticles
            ctx['viewer'] = author
            ctx['form'] = CommentForms(initial={'author': author,'article': article})
        return ctx
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        author = profilemodel.Profile.objects.get(user=self.request.user)
        article = self.get_object()
        form = CommentForms(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = author
            comment.article = article
            comment.save()
            return redirect('blog:article-detail', pk=article.pk)
        ctx = self.get_context_data(**kwargs)
        return self.render_to_response(ctx)
    
class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForms
    template_name = ''

    def get_success_url(self):
        return reverse_lazy('blog:article-detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        author = profilemodel.Profile.objects.get(user=self.request.user)
        form.instance.author = author
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        author = profilemodel.Profile.objects.get(user=self.request.user)
        ctx['form'] = ArticleForms(initial={'author': author})

    def get_initial(self):
        author = profilemodel.Profile.objects.get(user=self.request.user)
        return {'author':author}
    
class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForms
    template_name = ''

    def get_success_url(self):
        return reverse_lazy('blog:article-detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)