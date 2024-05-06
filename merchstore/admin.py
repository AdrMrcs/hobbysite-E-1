from django.contrib import admin
from merchstore.models import *

# Register your models here.

class ProductInline (admin.TabularInline):
    model = Product
    fields = ['name', 'description', 'price', 'producttype', ]

class ProductTypeAdmin (admin.ModelAdmin):
    model = ProductType

    search_fields = ('name', )
    list_display = ('name', 'description', 'id', )
    list_filter = ('name', )

    inlines = [ProductInline, ]

class ProductAdmin (admin.ModelAdmin):
    model = Product

    list_display = ('name', 'owner', 'status', 'description', 'price', 'producttype')

class TransactionAdmin (admin.ModelAdmin):
    model = Transaction

    list_display = ('buyer', 'product', 'amount', 'created_on', )

admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Transaction, TransactionAdmin)
