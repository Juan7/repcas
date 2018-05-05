from decimal import Decimal

from rest_framework import serializers

from . import models

def parse_discount(discount):
    return discount / 100


class ProductSerializer(serializers.ModelSerializer):

    calculated_price = serializers.SerializerMethodField()

    class Meta:

        model = models.Product
        fields = ('id', 'name', 'code', 'quantity', 'price', 'calculated_price',
                  'image', 'is_active', 'created_at')

    def get_calculated_price(self, obj):    
        base_price = obj.price

        product_distribution_channel = models.ProductDistributionChannel.objects.filter(
            product=obj, 
            distribution_channel=self.context['request'].profile.client.distribution_channel,
            is_active=True).first()

        if product_distribution_channel:
            base_price = product_distribution_channel.price

        laboratory_discount = obj.laboratory.discount
        
        special_finantial_discount = models.SpecialFinantialDiscount.objects.filter(
            client=self.context['request'].profile.client, laboratory=obj.laboratory).first()
        if special_finantial_discount:
            laboratory_discount = special_finantial_discount.discount
            
        base_price = base_price - (base_price * parse_discount(laboratory_discount))

        special_price = models.SpecialPrice.objects.filter(
            product=obj,
            client=self.context['request'].profile.client,
            is_active=True).first()
        if special_price:
            base_price = base_price - (base_price * parse_discount(special_price.discount))
        
        return base_price * Decimal('1.18')


class ProductPriceSerializer(serializers.ModelSerializer):

    calculated_price = serializers.SerializerMethodField()
    calculated_unit_price = serializers.SerializerMethodField()

    class Meta:

        model = models.Product
        fields = ('id', 'name', 'calculated_price', 'calculated_unit_price', 'is_active')

    def get_calculated_unit_price(self, obj):    
        base_price = obj.price
        quantity = self.context['request'].query_params.get('quantity', 0)

        distribution_channel = self.context['request'].profile.client.distribution_channel
        product_distribution_channel = models.ProductDistributionChannel.objects.filter(
            product=obj, 
            distribution_channel=distribution_channel,
            is_active=True).first()

        if product_distribution_channel:
            base_price = product_distribution_channel.price

        laboratory_discount = obj.laboratory.discount
        
        special_finantial_discount = models.SpecialFinantialDiscount.objects.filter(
                client=self.context['request'].profile.client, laboratory=obj.laboratory).first()
        if special_finantial_discount:
            laboratory_discount = special_finantial_discount.discount
            
        base_price = base_price - (base_price * parse_discount(laboratory_discount))

        scale = obj.productscale_set.filter(
            min_value__lte=quantity, max_value__gte=quantity, distribution_channel=distribution_channel, is_active=True).order_by('-start_date').first()
        
        if not scale:
            scale = obj.productscale_set.filter(
                min_value__lte=quantity, max_value=0, distribution_channel=distribution_channel, is_active=True).order_by('-start_date').first()
        
        if scale:
            base_price = base_price - (base_price * parse_discount(scale.discount))

        special_price = models.SpecialPrice.objects.filter(
            product=obj,
            client=self.context['request'].profile.client,
            is_active=True).first()
        if special_price:
            base_price = base_price - (base_price * parse_discount(special_price.discount))
        
        return base_price * Decimal('1.18')
    
    def get_calculated_price(self, obj):
        quantity = self.context['request'].query_params.get('quantity', 0)
        return Decimal(quantity) * self.get_calculated_unit_price(obj)


class ProductScaleSerializer(serializers.ModelSerializer):

    calculated_price = serializers.SerializerMethodField()

    class Meta:

        model = models.ProductScale
        fields = ('id', 'product', 'min_value', 'max_value', 'discount', 'calculated_price', 'is_active')
        
    def get_calculated_price(self, obj):
        base_price = obj.product.price

        distribution_channel = self.context['request'].profile.client.distribution_channel
        product_distribution_channel = models.ProductDistributionChannel.objects.filter(
            product=obj.product, 
            distribution_channel=distribution_channel,
            is_active=True).first()

        if product_distribution_channel:
            base_price = product_distribution_channel.price

        laboratory_discount = obj.product.laboratory.discount
        
        special_finantial_discount = models.SpecialFinantialDiscount.objects.filter(
            client=self.context['request'].profile.client, laboratory=obj.product.laboratory).first()
        if special_finantial_discount:
            laboratory_discount = special_finantial_discount.discount
            
        base_price = base_price - (base_price * parse_discount(laboratory_discount))

        special_price = models.SpecialPrice.objects.filter(
            product=obj.product,
            client=self.context['request'].profile.client,
            is_active=True).first()
        if special_price:
            base_price = base_price - (base_price * parse_discount(special_price.discount))

        base_price = base_price - (base_price * parse_discount(obj.discount))
        return Decimal('1.00') * base_price * Decimal('1.18')


class ProductPromotionSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)
    child_product = ProductSerializer(read_only=True)

    class Meta:

        model = models.ProductPromotion
        fields = ('id', 'product', 'product_quantity', 'child_product', 'child_product_quantity', 'is_active')
