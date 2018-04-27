import os
import uuid

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from accounts.models import Client, DistributionChannel


def get_file_path(instance, filename):
    """Get a random filename to avoid override on server."""
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4(), ext)
    return os.path.join('product/img', filename)


class Laboratory(models.Model):
    """Laboratory that produces a product's line."""
    name = models.CharField(max_length=254)
    code = models.CharField(max_length=11)

    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),
                                   validators=[MinValueValidator(Decimal('0.00'))])

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'[{self.code}] {self.name}'


class Product(models.Model):
    name = models.CharField(max_length=254)
    code = models.CharField(max_length=254)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),
                                   validators=[MinValueValidator(Decimal('0.00'))])
    price = models.DecimalField(max_digits=10, decimal_places=4,
                                validators=[MinValueValidator(Decimal('0.00'))])
    image = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'[{self.code}] {self.name}'
    

class ProductDistributionChannel(models.Model):
    """Distribution channel price for an specific product."""
    distribution_channel = models.ForeignKey(DistributionChannel, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=4,
                              validators=[MinValueValidator(Decimal('0.00'))])

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'[{self.distribution_channel.name}] {self.product.name}'


class ProductScale(models.Model):
    """Scale of products amount that has an special discount."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    min_value = models.IntegerField(default=1)
    max_value = models.IntegerField(default=1)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),
                                   validators=[MinValueValidator(Decimal('0.00'))])

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.product.name} [{self.min_value} - {self.max_value}]'


class ProductPromotion(models.Model):
    """Represent extra products that we can give selling a parent product"""
    product = models.ForeignKey(Product, related_name='parent', on_delete=models.CASCADE)
    product_quantity = models.IntegerField(default=1)
    child_product = models.ForeignKey(Product, related_name='child', on_delete=models.CASCADE)
    child_product_quantity = models.IntegerField(default=1)

    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.product_quantity} {self.product.name} + {self.child_product_quantity} {self.child_product.name}'


class SpecialPrice(models.Model):
    """Special discount for a product and a client."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),
                                   validators=[MinValueValidator(Decimal('0.00'))])

    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.product.name} - {self.client.name} ({self.discount})'
