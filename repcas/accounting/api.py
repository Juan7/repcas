import django_filters
from rest_framework import permissions, response, status, viewsets, filters

from main import pagination
from . import models, serializers


class InvoiceViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.InvoiceSerializer

    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter)
    queryset = models.Invoice.objects.all()
    filter_fields = {
        'number': ['icontains']
    }


class QuotationViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.QuotationSerializer

    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter)
    queryset = models.Quotation.objects.all()
    filter_fields = {
        'number': ['icontains']
    }
