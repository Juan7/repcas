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
    pdf_promotion = models.WebPdfPromotion.objects.order_by('-id').first()
    context = {
        'promotions': promotions,
        'pdf_promotion': pdf_promotion
    }
    return render(request, 'main/promociones.html', context)


@login_required
def app(request):
    context = {'agent': settings.AGENT_EMAIL}
    return render(request, 'main/app/app.html', context)


def update(request):
#    result = functions.update_distribution_channel()
#    result = functions.update_laboratory()
#    result = functions.update_clients()
    result = functions.update_invoices()
#    result = functions.update_products()
#    result = functions.update_distribution_channel_price()
#    result = functions.update_promotions()
#    result = functions.update_scales_price()
#    result = functions.update_special_finantial_discount()
#    result = functions.update_special_price()
    context = {
        'result': result
    }
    return render(request, 'main/update.html', context)
