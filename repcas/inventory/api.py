import operator
from copy import copy
from functools import reduce

import django_filters

from django.db.models import Q

from rest_framework import permissions, response, status, viewsets, filters

from main import pagination
from . import models, serializers


class ProductViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ProductSerializer

    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter)
    queryset = models.Product.objects.all()
    
    filter_fields = {
        'name': ['icontains'],
        'code': ['icontains']
    }
    
    def filter_queryset(self, queryset):
        print(self.request.query_params)
        if self.request.query_params.get('name__icontains'):
            query_params = copy(self.request.query_params)
            params = [Q(**{name: value})
                      for name, value in query_params.items()
                      if name != 'condition']
            queryset = queryset.filter(reduce(operator.or_, params))

        else:
            queryset = super().filter_queryset(queryset)
        return queryset

    
class ProductPromotionViewSet(viewsets.ModelViewSet):
    
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ProductPromotionSerializer

    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter)
    queryset = models.ProductPromotion.objects.all()
    
    filter_fields = {
        'product__id': ['exact'],
    }
    

class ProductScaleViewSet(viewsets.ModelViewSet):
    
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ProductScaleSerializer

    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter)
    queryset = models.ProductScale.objects.all()
    
    filter_fields = {
        'product__id': ['exact'],
    }


class ProductPriceViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ProductPriceSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter)
    queryset = models.Product.objects.all()

    # def retrieve(self, request, pk=None):
    #     print(self.request.data)
    #     return super().retrieve(request, pk)
