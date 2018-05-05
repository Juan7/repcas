from rest_framework import serializers
from django.utils import timezone
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
    days = serializers.SerializerMethodField()
    amount_pending = serializers.SerializerMethodField()

    class Meta:

        model = models.Invoice
        fields = ('id', 'items', 'client', 'date', 'number', 'total', 'is_payed',
                  'due_date', 'document_type', 'amount_payed', 'unique_code', 
                  'amount_pending', 'state', 'is_active', 'created_at', 'days')

    def get_days(self, obj):
        return (obj.due_date - timezone.now()).days

    def get_amount_pending(self, obj):
        return obj.total - obj.amount_payed


class QuotationItemSerializer(serializers.ModelSerializer):
    product_display = serializers.SerializerMethodField()

    class Meta:

        model = models.QuotationItem
        fields = ('id', 'quotation', 'product', 'quantity',
                  'price', 'total', 'is_active', 'created_at', 'product_display')
        extra_kwargs = {
            'quotation': {'required': False}
        }

    def get_product_display(self, obj):
        return obj.product.name


class QuotationSerializer(serializers.ModelSerializer):
    items = QuotationItemSerializer(many=True)

    class Meta:

        model = models.Quotation
        fields = ('id', 'items', 'client', 'date', 'number', 'total',
                  'state', 'is_active', 'created_at')

        extra_kwargs = {
            'client': {'required': False},
            'number': {'required': False}
        }

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        validated_data['client'] = self.context['request'].profile.client
        quotation = models.Quotation.objects.create(**validated_data)

        for item_data in items_data:
            models.QuotationItem.objects.create(quotation=quotation, **item_data)

        return quotation


class QuotationMinSerializer(serializers.ModelSerializer):

    class Meta:

        model = models.Quotation
        fields = ('id', 'date', 'number', 'total')
