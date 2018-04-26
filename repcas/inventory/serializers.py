from rest_framework import serializers

from . import models


class ProductSerializer(serializers.ModelSerializer):

    class Meta:

        model = models.Product
        fields = ('id', 'name', 'code', 'quantity', 'price',
                  'image', 'is_active', 'created_at')
