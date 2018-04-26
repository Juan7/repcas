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
