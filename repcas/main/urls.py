from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views

app_name = 'main'

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='app')),
    url(r'^app/$', views.app, name='app')
]
