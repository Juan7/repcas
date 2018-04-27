from django.contrib import admin

from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Laboratory)
class LaboratoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProductDistributionChannel)
class ProductDistributionChannelAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProductScale)
class ProductScaleAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProductPromotion)
class ProductPromotionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.SpecialPrice)
class SpecialPriceAdmin(admin.ModelAdmin):
    pass

