from django.db import models

# Create your models here.

class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return '{}'.format(self.name)
    
class Article(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        ArticleCategory,
        on_delete = models.SET_NULL
    )
    entry = models.TextField

    def __str__(self):
        return '{}'.format(self.title)