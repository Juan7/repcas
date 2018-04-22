from rest_framework import serializers

from . import models


class InvoiceItemSerializer(serializers.ModelSerializer):

    class Meta:

        model = models.InvoiceItem
        fields = ('id', 'invoice', 'product', 'quantity',
                  'price', 'total', 'is_active', 'created_at')


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)

    class Meta:

        model = models.Invoice
        fields = ('id', 'items', 'client', 'date', 'number', 'total', 'is_payed',
                  'state', 'is_active', 'created_at')
