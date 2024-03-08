from django.urls import path

from .views import CommissionListView, CommissionDetailView

urlpatterns = [
    path('commission/list', CommissionListView.as_view(), name='commission-list'),
    path('commission/detail/<int:pk>', CommissionDetailView.as_view(), name='commission-detail')
]

app_name = 'commission'