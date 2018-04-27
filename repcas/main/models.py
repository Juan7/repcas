import os
import uuid

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


def get_file_path(instance, filename):
    """Get a random filename to avoid override on server."""
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4(), ext)
    return os.path.join('web/img', filename)


class WebPromotion(models.Model):
    name = models.CharField(max_length=254)
    code = models.CharField(max_length=254, blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),
                                   validators=[MinValueValidator(Decimal('0.00'))])
    price = models.DecimalField(max_digits=10, decimal_places=4,
                                validators=[MinValueValidator(Decimal('0.00'))])
    image = models.ImageField(upload_to=get_file_path, blank=True, null=True)

    title = models.CharField(max_length=254, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'
