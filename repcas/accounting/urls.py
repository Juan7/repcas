from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api

app_name = 'accounting'

router = DefaultRouter()
router.register('invoices', api.InvoiceViewSet, base_name='api_invoice')
router.register('quotations', api.QuotationViewSet, base_name='api_quotation')

apipatterns = router.urls + []

urlpatterns = [
    path('api/', include(apipatterns)),
]
