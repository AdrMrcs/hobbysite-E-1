from django.urls import path

from .views import WikiListView, WikiDetailView


urlpatterns = [
    path("articles", WikiListView.as_view(), name="article_list"),
    path("articles/<int:pk>", WikiDetailView.as_view(), name="article_details"),
]

app_name = "wiki"
