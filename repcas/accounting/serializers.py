from rest_framework import serializers

from . import models
from accounts.serializers import ClientSerializer


class InvoiceItemSerializer(serializers.ModelSerializer):

    class Meta:

        model = models.InvoiceItem
        fields = ('id', 'invoice', 'product', 'quantity',
                  'price', 'total', 'is_active', 'created_at')


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)
    client = ClientSerializer(many=False)

    class Meta:

        model = models.Invoice
        fields = ('id', 'items', 'client', 'date', 'number', 'total', 'is_payed',
                  'state', 'is_active', 'created_at')


class QuotationItemSerializer(serializers.ModelSerializer):

    class Meta:

        model = models.QuotationItem
        fields = ('id', 'quotation', 'product', 'quantity',
                  'price', 'total', 'is_active', 'created_at')


class QuotationSerializer(serializers.ModelSerializer):
    items = QuotationItemSerializer(many=True)

    class Meta:

        model = models.Quotation
        fields = ('id', 'items', 'client', 'date', 'number', 'total',
                  'state', 'is_active', 'created_at')
