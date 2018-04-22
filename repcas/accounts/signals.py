from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models

@receiver(user_logged_out, sender=User)
def delete_auth_token(sender, user, request, **kwargs):
    """Destroy the authorization token cookie."""
    cookie = {'key': 'client_pk'}

    try:
        request.delete_cookies
    except AttributeError:
        request.delete_cookies = []
    request.delete_cookies.append(cookie)
