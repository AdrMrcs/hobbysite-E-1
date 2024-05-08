from django.forms.models import BaseModelForm
from django.http.request import HttpRequest as HttpRequest
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.urls import reverse_lazy, reverse

from .models import ProductType, Product
from user_management.models import Profile

# Create your views here.

class ProductListView (ListView):
    model = Product
    template_name = 'product_list.html'

# Source(s): Django Documentation
class ProductDetailView (CreateView):
    model = Product
    form_class = TransactionForm
    template_name = 'product_detail.html'

    def get_success_url(self):
        return reverse_lazy('merchstore:cart-view')

    def setup(self, request, *args, **kwargs):
        self.pk = kwargs['pk']
        self.username = request.user.username
        return super().setup(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['object'] = Product.objects.get(id=self.pk)
        return kwargs
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['pk'] = self.pk
        kwargs['user'] = self.username
        return kwargs
    
    def post(self, request: HttpRequest, *args, **kwargs):
        product = Product.objects.get(id=self.pk)
        amount = int(request.POST.get('amount'))
        buyer = Profile.objects.get(id=request.POST.get('buyer'))
        update_stock(product, amount)
        add_transaction(buyer, product, amount)
        return HttpResponseRedirect(self.get_success_url())
        
def update_stock (product: Product, amount: int):
    product.stock -= amount
    if product.stock <= 0:
        product.status = 'Out of Stock'
    product.save()

def add_transaction (buyer: Profile, product: Product, amount: int):
    t = Transaction()
    t.buyer = buyer
    t.product = product
    t.amount = amount
    t.save()

class ProductCreateView (LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'

    def get_success_url(self):
        return reverse_lazy('merchstore:product-detail')
    
class ProductUpdateView (LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'

    def get_success_url(self):
        return reverse_lazy('merchstore:product-detail', kwargs={ 'pk': self.pk })

    def setup(self, request, *args, **kwargs):
        self.pk = kwargs['pk']
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=self.pk)
        update_product(product, request)
        return HttpResponseRedirect(self.get_success_url())

def update_product (product: Product, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = int(request.POST.get('stock'))
        owner = Profile.objects.get(id=request.POST.get('owner'))
        producttype = ProductType.objects.get(id=request.POST.get('producttype'))
        product.name = name
        product.description = description
        product.price = price
        product.stock = stock
        product.owner = owner
        producttype = producttype
        if stock > 0:
            product.status = 'Available'
        else:
            product.status = 'Out of Stock'
        product.save()
    
class CartView (LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'cart_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profiles'] = Profile.objects.all()
        return context

class TransactionView (LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transaction_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profiles'] = Profile.objects.all()
        return context