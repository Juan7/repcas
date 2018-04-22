from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers

from . import models


class ClientSerializer(serializers.ModelSerializer):
    """Client model serializer."""

    class Meta:
        """Client serializer meta data."""

        model = models.Client
        fields = ('id', 'name', 'image', 'ruc',
                  'address', 'email', 'phone', 'is_active')


class ProfileSerializer(serializers.ModelSerializer):
    """Profile model serializer."""

    class Meta:
        """Profile serializer meta data."""

        model = models.Profile
        fields = ('id', 'user', 'client', 'phone', 'is_active')


class AgentSerializer(serializers.ModelSerializer):
    """Agent model serializer."""

    class Meta:
        """Agent serializer meta data."""

        model = models.Agent
        fields = ('id', 'name', 'client', 'address', 'email', 'phone', 'is_active')
