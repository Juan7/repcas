from django.contrib import admin

from . import models


@admin.register(models.WebPromotion)
class WebPromotionAdmin(admin.ModelAdmin):
    pass
