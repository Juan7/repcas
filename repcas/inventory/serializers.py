from decimal import Decimal

from rest_framework import serializers

from . import models


class ProductSerializer(serializers.ModelSerializer):

    class Meta:

        model = models.Product
        fields = ('id', 'name', 'code', 'quantity', 'price',
                  'image', 'is_active', 'created_at')
        

class ProductPriceSerializer(serializers.ModelSerializer):

    calculated_price = serializers.SerializerMethodField()

    class Meta:

        model = models.Product
        fields = ('id', 'name', 'calculated_price', 'is_active')
        
    def get_calculated_price(self, obj):
        base_price = obj.price
        quantity = self.context['request'].query_params.get('quantity', 0)

        product_distribution_channel = models.ProductDistributionChannel.objects.filter(
            product=obj, 
            distribution_channel=self.context['request'].profile.client.distribution_channel,
            is_active=True).first()
        if product_distribution_channel:
            base_price = product_distribution_channel.price
        
        if obj.laboratory.discount:
            base_price = base_price - (base_price * obj.laboratory.discount)
        
        scale = obj.productscale_set.filter(
            min_value__lte=quantity, max_value__gte=quantity, is_active=True).order_by('-start_date').first()
        if scale:
            base_price = base_price - (base_price * scale.discount)
            
        special_price = models.SpecialPrice.objects.filter(
            product=obj, 
            client=self.context['request'].profile.client,
            is_active=True).first()
        if special_price:
            base_price = base_price - (base_price * special_price.discount)

        return Decimal(quantity) * base_price * Decimal('1.18')

        
class ProductScaleSerializer(serializers.ModelSerializer):
    
    discount_display = serializers.SerializerMethodField()
    
    class Meta:
        
        model = models.ProductScale
        fields = ('id', 'product', 'min_value', 'max_value', 'discount', 'discount_display', 'is_active')

    def get_discount_display(self, obj):
        return obj.discount * Decimal('100')


class ProductPromotionSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)
    child_product = ProductSerializer(read_only=True)
    
    class Meta:

        model = models.ProductPromotion
        fields = ('id', 'product', 'product_quantity', 'child_product', 'child_product_quantity', 'is_active')
