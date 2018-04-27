from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from django.template import loader
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from accounts.models import Agent
from django.shortcuts import get_object_or_404
from django.conf import settings

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


def join(request):
    context = {}
    if request.method == 'POST':
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain

        context = {
            'domain': domain,
            'protocol': 'https' if request.is_secure() else 'http',
            'email': request.POST.get('email'),
            'full_name': request.POST.get('full_name'),
            'ruc': request.POST.get('ruc')
        }

        from_email = f'{site_name} Team <no-reply@{domain}>'

        to_email = settings.JOIN_EMAIL
        subject = 'Solicitud de usuario.'

        template = loader.get_template('accounts/join_email.html')
        message = template.render(context)

        send_mail(subject, '', from_email, [to_email], fail_silently=True, html_message=message)

    return render(request, 'registration/join.html', context)


class MakeOrder(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain

        agent = get_object_or_404(Agent, id=request.data.get('agent_id'))
        products_data = request.data.get('products')
        total = 0
        for product in products_data:
            total += float(product['price'])

        context = {
            'agent': agent,
            'domain': domain,
            'protocol': 'https' if request.is_secure() else 'http',
            'products': products_data,
            'total': total
        }

        from_email = f'{site_name} Team <no-reply@{domain}>'

        to_email = agent.email
        subject = 'Pedido'

        template = loader.get_template('accounts/order_email.html')
        message = template.render(context)

        send_mail(subject, '', from_email, [to_email], fail_silently=True, html_message=message)
        return Response()
