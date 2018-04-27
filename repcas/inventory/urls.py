from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api

app_name = 'inventory'

router = DefaultRouter()
router.register('products', api.ProductViewSet, base_name='api_product')
router.register('product-promotions', api.ProductPromotionViewSet, base_name='api_product_promotions')
router.register('product-scales', api.ProductScaleViewSet, base_name='api_product_scales')
router.register('check-product-price', api.ProductPriceViewSet, base_name='api_product_price')

apipatterns = router.urls + []

urlpatterns = [
    path('api/', include(apipatterns)),
]
