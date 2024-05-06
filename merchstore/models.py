from django.db import models
from django.urls import reverse

from user_management.models import Profile

# Create your models here.

class ProductType (models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__ (self):
        return self.name
    
    class Meta:
        ordering = ['name', ]
        verbose_name = 'Product Type'

class Product (models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    status_choices = [
        ('Available', 'Available'), 
        ('On Sale', 'On Sale'), 
        ('Out of Stock', 'Out of Stock')
    ]
    status = models.CharField (
        max_length=50, 
        choices=status_choices, 
        default='Available', 
    )

    owner = models.ForeignKey (
        Profile, 
        on_delete=models.CASCADE, 
        null=True, 
        related_name = 'profile'
    )

    producttype = models.ForeignKey (
        ProductType, 
        null = True, 
        on_delete=models.SET_NULL, 
        related_name = 'products', 
        verbose_name = 'Product Type', 
    )

    def __str__ (self):
        return self.name

    def get_absolute_url(self):
        return reverse('merchstore:product-detail', args=[self.pk])

    class Meta:
        ordering = ['name', ]

class Transaction (models.Model): 
    buyer = models.ForeignKey (
        Profile, 
        on_delete=models.SET_NULL, 
        null=True, 
    )
    product = models.ForeignKey (
        Product, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name= 'products'
    )
    amount = models.IntegerField(default=0)
    status_choices = [
        ('On Cart', 'On Cart'), 
        ('To Pay', 'To Pay'), 
        ('To Ship', 'To Ship'), 
        ('To Receive', 'To Receive'), 
        ('Delivered', 'Delivered'), 
    ]
    status = models.CharField (
        max_length=50, 
        choices=status_choices, 
        default = 'On Cart', 
    )
    created_on = models.DateTimeField(auto_now_add=True)