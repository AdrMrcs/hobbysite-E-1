from django.urls import path

from .views import *

urlpatterns = [
    path('items', ProductListView.as_view(), name='product-list'),
    path('item/<int:pk>', ProductDetailView.as_view(), name='product-detail'), 
    path('item/add', ProductCreateView.as_view(), name='create-view'), 
    path('item/<int:pk>/edit', ProductUpdateView.as_view(), name='update_view'),
    path('cart', CartView.as_view(), name='cart-view'), 
    path('transactions', TransactionView.as_view(), name='transaction-view')
]

app_name = "merchstore"