from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .functions import set_cookie

from . import models


@login_required
def client_login_redirect(request):
    profile = models.Profile.objects.select_related(
            'user', 'client'
        ).filter(
            user=request.user,
            is_active=True,
            client__is_active=True).first()
    # import pdb; pdb.set_trace()
    if profile:
        set_cookie(request, 'client_pk', profile.client.id)
        return redirect(reverse('main:app'))
    return redirect(reverse('accounts:non_user_client'))


@login_required
def non_user_client(request):
    context = {
        'message': 'Su usuario aún no cuenta con un cliente asociado. Comuníquese con Representaciones Castillo para resolver este invonveniente.'
    }
    return render(request, 'registration/non_user_client.html', context)