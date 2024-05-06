from django.db import models
from django.urls import reverse

from user_management.models import Profile

class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]


class Article(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        default=1,
        related_name="articleauthor"
    )
    category = models.ForeignKey(
        "ArticleCategory",
        on_delete=models.SET_NULL,
        null=True,
        default=1,
        related_name="articlecategory"
    )
    entry = models.TextField
    headerImage = models.ImageField(upload_to="images/", null=False)
    createdOn = models.DateTimeField(auto_now_add=True)
    updatedOn = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Title: {self.title} Category: {self.category} Created on: {self.createdOn} Updated on: {self.updatedOn}"

    def get_absolute_url(self):
        return reverse("wiki:article_details", args=[self.pk])

    class Meta:
        ordering = ["-createdOn"]

class Comment(models.Model):
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        default=1,
        related_name="commentauthor"
    )
    article = models.ForeignKey(
        "ArticleCategory",
        on_delete=models.CASCADE,
        default=1,
        related_name="commentarticle"
    )
    entry = models.TextField
    createdOn = models.DateTimeField(auto_now_add = True)
    updatedOn = models.DateTimeField(auto_now = False)

    class Meta:
        ordering = ["createdOn"]