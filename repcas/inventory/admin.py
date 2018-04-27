from django.contrib import admin

from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Laboratory)
class LaboratoryAdmin(admin.ModelAdmin):
    pass
