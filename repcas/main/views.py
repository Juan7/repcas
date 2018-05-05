from django.template import loader
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
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
#    result = functions.update_invoices()
#    result = functions.update_products()
#    result = functions.update_distribution_channel_price()
#    result = functions.update_promotions()
#    result = functions.update_scales_price()
#    result = functions.update_special_finantial_discount()
    result = functions.update_special_price()
    context = {
        'result': result
    }
    return render(request, 'main/update.html', context)


def contact_us(request):
    if request.method == 'POST':
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain

        context = {
            'domain': domain,
            'protocol': 'https' if request.is_secure() else 'http',
            'full_name': request.POST.get('full_name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'business': request.POST.get('business')
        }

        from_email = f'{site_name} Team <no-reply@{domain}>'

        to_email = settings.JOIN_EMAIL
        subject = 'Solicitud de contacto.'

        template = loader.get_template('accounts/contact_email.html')
        message = template.render(context)

        send_mail(subject, '', from_email, [to_email], fail_silently=True, html_message=message)

    return redirect('/')
