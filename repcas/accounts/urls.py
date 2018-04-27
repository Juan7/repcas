from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api, views

app_name = 'accounts'

router = DefaultRouter()
router.register('client', api.ClientViewSet, base_name='api_client')
router.register('profile', api.ProfileViewSet, base_name='api_profile')
router.register('agent', api.AgentViewSet, base_name='api_agent')

apipatterns = router.urls + [

]

urlpatterns = [
    path('api/', include(apipatterns)),
    path('client-redirect/', views.client_login_redirect, name='client_login_redirect'),
    path('usuario-sin-cliente/', views.non_user_client, name='non_user_client')
]
