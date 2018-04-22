from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api

app_name = 'accounts'

router = DefaultRouter()
router.register('client', api.ClientViewSet, base_name='api_client')
router.register('profile', api.ProfileViewSet, base_name='api_profile')
router.register('agent', api.AgentViewSet, base_name='api_agent')

apipatterns = router.urls + [

]

urlpatterns = [
    path('api/', include(apipatterns)),
]
