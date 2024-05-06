from django.db import models
from django.urls import reverse

from user_management import models as profilemodel

class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return '{}'.format(self.name)
    
    def get_absolute_url(self):
        return reverse('blog:article-list', args=[self.pk])
    
    class Meta:
        ordering = ['name',]
    
class Article(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
    profilemodel.Profile,
    on_delete=models.SET_NULL,
    related_name='article_authors',
    null=True
    )
    category = models.ForeignKey(
        'ArticleCategory',
        on_delete = models.SET_NULL,
        related_name = 'articles',
        null = True
    )
    entry = models.TextField()
    headerimage = models.ImageField(upload_to='images/', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.title)
    
    def get_absolute_url(self):
        return reverse('blog:article-detail', args=[self.pk])
    
    class Meta:
        ordering = ['created_on']

class Comment(models.Model):
    author = models.ForeignKey(
    profilemodel.Profile,
    on_delete=models.SET_NULL,
    related_name='comment_authors',
    null=True
    )
    article = models.ForeignKey(
    Article,
    on_delete=models.CASCADE,
    related_name='comments',
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_on',]