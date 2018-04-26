import django_filters
import json
import operator
from copy import copy
from functools import reduce

from django.db.models import Q
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
        'is_payed': ['exact'],
        'number': ['icontains'],
        'client__name': ['icontains']
    }

    def filter_queryset(self, queryset):
        print(self.request.query_params)
        if self.request.query_params.get('number__icontains'):
            query_params = copy(self.request.query_params)
            if query_params.get('is_payed'):
                queryset = queryset.filter(
                    is_payed=json.loads(query_params.get('is_payed')))
                query_params.pop('is_payed')
            params = [Q(**{name: value})
                      for name, value in query_params.items()
                      if name != 'condition']
            print(reduce(operator.or_, params))

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
