from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import ProductType, Product

# Create your views here.

def merch_list (request):
    ctx = {
        "products": ProductType.objects.all(), 
    }
    return render (request, 'product_list.html', ctx)

def merch_detail (request, id):
    ctx = {
        "producttype": ProductType.objects.get(id=id), 
        "products": Product.objects.filter(producttype__id=id), 
    }
    return render (request, 'product_detail.html', ctx)

class ProductListView (ListView):
    model = ProductType
    template_name = 'product_list.html'

class ProductDetailView (DetailView):
    model = ProductType
    template_name = 'product_detail.html'