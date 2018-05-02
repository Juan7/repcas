import django_filters
from rest_framework import permissions, response, status, viewsets, filters

from main import pagination
from . import models, serializers


class ClientViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ClientSerializer

    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter)
    queryset = models.Client.objects.all()

    filter_fields = {
        'name': ['icontains'],
        'ruc': ['icontains']
    }


class ProfileViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ProfileSerializer

    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter)

    queryset = models.Profile.objects.all()
    filter_fields = {
        'user__username': ['icontains']
    }
