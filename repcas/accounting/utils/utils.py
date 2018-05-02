from django.template import loader
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings


def make_order(request, quotation):
    current_site = get_current_site(request)
    site_name = current_site.name
    domain = current_site.domain

    context = {
        'domain': domain,
        'protocol': 'https' if request.is_secure() else 'http',
        'products': quotation.items.all(),
        'total': quotation.total,
        'client': quotation.client.name,
    }

    from_email = f'{site_name} Team <no-reply@{domain}>'

    to_email = settings.AGENT_EMAIL
    subject = 'Pedido'

    template = loader.get_template('accounts/order_email.html')
    message = template.render(context)

    return send_mail(subject, '', from_email, [to_email], fail_silently=True, html_message=message)
