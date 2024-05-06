from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .models import *
from user_management.models import Profile

class TransactionForm (forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', ]
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.pk = kwargs.pop('pk')
        self.product = Product.objects.filter(id=self.pk)
        stock = self.product[0].stock
        self.fields['amount'].widget.attrs.update ({'max': stock,'min': 0})
        

class ProductForm (forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'