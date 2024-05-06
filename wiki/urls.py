from django.urls import path

from .views import WikiListView, WikiDetailView, CreateWikiArticle, EditWikiArticle


urlpatterns = [
    path("articles", WikiListView.as_view(), name="article_list"),
    path("articles/<int:pk>", WikiDetailView.as_view(), name="article_details"),
    path('article/add', CreateWikiArticle.as_view(), name='article_create'),
    path('article/<int:pk>/edit', EditWikiArticle.as_view(), name='article_edit'),
]

app_name = "wiki"
