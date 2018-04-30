import django_filters
import json
import operator
from copy import copy
from functools import reduce

from django.db.models import Q
from rest_framework import permissions, response, status, viewsets, filters

from main import pagination
from . import models, serializers
from .utils import utils


class InvoiceViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.InvoiceSerializer

    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter)
    queryset = models.Invoice.objects.all()
    filter_fields = {
        'is_payed': ['exact'],
        'number': ['icontains'],
        'client__name': ['icontains']
    }

    def get_queryset(self):
        client = self.request.profile.client
        return models.Invoice.objects.filter(is_active=True, client=client)

    def filter_queryset(self, queryset):
        if self.request.query_params.get('number__icontains'):
            query_params = copy(self.request.query_params)
            if query_params.get('is_payed'):
                queryset = queryset.filter(
                    is_payed=json.loads(query_params.get('is_payed')))
                query_params.pop('is_payed')
            params = [Q(**{name: value})
                      for name, value in query_params.items()
                      if name != 'condition']

            queryset = queryset.filter(reduce(operator.or_, params))

        else:
            queryset = super().filter_queryset(queryset)
        return queryset


class QuotationViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.QuotationSerializer

    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter)
    queryset = models.Quotation.objects.all()
    filter_fields = {
        'number': ['icontains']
    }

    def get_serializer_class(self):
        pk = self.kwargs.get('pk')
        if self.request.method == 'GET' and not pk:
            return serializers.QuotationMinSerializer

        return serializers.QuotationSerializer

    def perform_create(self, serializer):
        quotation = serializer.save()
        utils.make_order(self.request, quotation)
