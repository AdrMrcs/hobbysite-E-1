from django.db import models
from django.urls import reverse

class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        ordering = ['name']

class Article(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey('ArticleCategory',
        on_delete = models.SET_NULL,
        null = True,
        default = 1,
        related_name = "articlecategory"
    )
    createdOn = models.DateTimeField(auto_now_add = True)
    updatedOn = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f'Title: {self.title} Category: {self.category} Created on: {self.createdOn} Updated on: {self.updatedOn}'
    def get_absolute_url(self):
        return reverse('wiki:article_details', args=[self.pk])
    
    class Meta:
        ordering = ['-createdOn']

# Create your models here.
