from decimal import Decimal

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from accounts.models import Client
from inventory.models import Product


class Invoice(models.Model):
    WAITING = 1
    CONFIRMED = 2

    STATE_CHOICES = (
        (WAITING, 'Esperando'),
        (CONFIRMED, 'Confirmado'),
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    number = models.CharField(max_length=254)
    document_type = models.CharField(max_length=5, default='01')
    date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=4, default=Decimal('0.00'),
                                validators=[MinValueValidator(Decimal('0.00'))])
    amount_payed = models.DecimalField(max_digits=10, decimal_places=4, default=Decimal('0.00'),
                                validators=[MinValueValidator(Decimal('0.00'))])
    unique_code = models.CharField(max_length=254, blank=True)
    
    is_payed = models.BooleanField(default=False)
    state = models.IntegerField(choices=STATE_CHOICES, default=WAITING, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.number


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),
                                   validators=[MinValueValidator(Decimal('0.00'))])
    price = models.DecimalField(max_digits=10, decimal_places=4,
                                validators=[MinValueValidator(Decimal('0.00'))])
    total = models.DecimalField(max_digits=10, decimal_places=4,
                                validators=[MinValueValidator(Decimal('0.00'))])

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name


class Quotation(models.Model):
    WAITING = 1
    CONFIRMED = 2

    STATE_CHOICES = (
        (WAITING, 'Esperando'),
        (CONFIRMED, 'Confirmado'),
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    number = models.CharField(max_length=254)
    total = models.DecimalField(max_digits=10, decimal_places=4,
                                validators=[MinValueValidator(Decimal('0.00'))])
    state = models.IntegerField(choices=STATE_CHOICES, default=WAITING, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.number

    def save(self, *args, **kwargs):
        self.number = type(self).objects.count() + 1
        super().save(*args, **kwargs)


class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),
                                   validators=[MinValueValidator(Decimal('0.00'))])
    price = models.DecimalField(max_digits=10, decimal_places=4,
                                validators=[MinValueValidator(Decimal('0.00'))])
    total = models.DecimalField(max_digits=10, decimal_places=4,
                                validators=[MinValueValidator(Decimal('0.00'))])

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name
