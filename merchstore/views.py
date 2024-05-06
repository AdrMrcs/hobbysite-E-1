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

    def setup(self, request: HttpRequest, *args, **kwargs):
        self.pk = kwargs['pk']
        if hasattr(request, 'user'):
            self.username = request.user.username
        return super().setup(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['object'] = Product.objects.get(id=self.pk)
        return kwargs
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['pk'] = self.pk
        if hasattr(self, 'username'):
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
        return reverse_lazy('merchstore:product-detail', kwargs={ 'pk': self.object.pk })
    
class ProductUpdateView (LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'

    def get_success_url(self):
        return reverse_lazy('merchstore:product-detail', kwargs={ 'pk': self.object.pk })
    
class CartView (LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'cart_view.html'

class TransactionView (LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transaction_view.html'