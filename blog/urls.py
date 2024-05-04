from django.urls import path

from .views import BlogDetailView, BlogListView


urlpatterns = [
    path('articles', BlogListView.as_view(), name='article-list'),
    path('article/<int:pk>', BlogDetailView.as_view(), name='article-detail'),
]

app_name = 'blog'