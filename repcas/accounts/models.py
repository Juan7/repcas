import os
import uuid

from django.db import models
from django.contrib.auth.models import User


def get_file_path(instance, filename):
    """Get a random filename to avoid override on server."""
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4(), ext)
    return os.path.join('user/avatar', filename)


class Client(models.Model):
    name = models.CharField(max_length=254)
    image = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    ruc = models.CharField(max_length=11)

    address = models.CharField(max_length=254)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Agent(models.Model):
    name = models.CharField(max_length=254)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    address = models.CharField(max_length=254)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
