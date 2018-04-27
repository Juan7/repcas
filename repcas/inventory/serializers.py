from rest_framework import serializers

from . import models


class ProductSerializer(serializers.ModelSerializer):

    class Meta:

        model = models.Product
        fields = ('id', 'name', 'code', 'quantity', 'price',
                  'image', 'is_active', 'created_at')

        
class ProductScaleSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = models.ProductScale
        fields = ('id', 'product', 'min_value', 'max_value', 'discount', 'is_active')


class ProductPromotionSerializer(serializers.ModelSerializer):

    parent = ProductSerializer(read_only=True)
    child = ProductSerializer(read_only=True)
    
    class Meta:

        model = models.ProductPromotion
        fields = ('id', 'parent', 'product_quantity', 'child', 'child_product_quantity', 'is_active')
