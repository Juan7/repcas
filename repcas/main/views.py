from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from . import models


def home(request):
    context = {}
    return render(request, 'main/index.html', context)


def promotions(request):
    promotions = models.WebPromotion.objects.filter(is_active=True).order_by('-created_at')
    context = {
        'promotions': promotions
    }
    return render(request, 'main/promociones.html', context)


@login_required
def app(request):
    return render(request, 'main/app/app.html', locals())
