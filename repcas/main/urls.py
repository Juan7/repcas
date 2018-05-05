from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views

app_name = 'main'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^promociones/$', views.promotions, name='promotions'),
    url(r'^update/$', views.update, name='update'),
    url(r'^app/$', views.app, name='app'),
    url(r'^contact-us/$', views.contact_us, name='contact_us')
]
