from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from . import functions
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
    context = {'agent': settings.AGENT_EMAIL}
    return render(request, 'main/app/app.html', context)


def update(request):
#    result = functions.update_distribution_channel()
    result = functions.update_laboratory()
    context = {
        'result': result
    }
    return render(request, 'main/update.html', context)
