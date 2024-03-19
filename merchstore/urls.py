from django.urls import path

from .views import merch_list, merch_detail, ProductListView, ProductDetailView

urlpatterns = [
    path('items', ProductListView.as_view(), name='product-list'),
    path('item/<int:pk>', ProductDetailView.as_view(), name='product-detail'), 
]

app_name = "merchstore"