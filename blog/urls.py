from django.urls import path

from .views import BlogDetailView, BlogListView

urlpatterns = [
    path('blog/articles', BlogListView.as_view(), name='article-list'),
    path('blog/article/<int:pk>', BlogDetailView.as_view(), name='article-detail')
]