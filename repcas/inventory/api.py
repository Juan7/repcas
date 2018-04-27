import django_filters
from rest_framework import permissions, response, status, viewsets, filters

from main import pagination
from . import models, serializers


class ProductViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ProductSerializer

    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter)
    queryset = models.Product.objects.all()

    
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
