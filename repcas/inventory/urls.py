from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api

app_name = 'inventory'

router = DefaultRouter()
router.register('products', api.ProductViewSet, base_name='api_product')

apipatterns = router.urls + []

urlpatterns = [
    path('api/', include(apipatterns)),
]
