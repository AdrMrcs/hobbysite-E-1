from django.urls import path

from .views import BlogDetailView, BlogListView, BlogCreateView, BlogUpdateView


urlpatterns = [
    path('articles', BlogListView.as_view(), name='article-list'),
    path('article/<int:pk>', BlogDetailView.as_view(), name='article-detail'),
    path('article/add', BlogCreateView.as_view(), name='article-create'),
    path('article/<int:pk>/edit', BlogUpdateView.as_view(), name='article-edit'),
]

app_name = 'blog'