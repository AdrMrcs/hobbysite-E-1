from django.urls import path

from .views import index, WikiListView, WikiDetailView 

urlpatterns = [
    path('', index, name="index"),
    path('articles', WikiListView.as_view(), name="article_list"),
    path('articles/<int:pk>', WikiDetailView.as_view(), name='article_details'),
]

app_name = "wiki"