from django.contrib import admin

from . import models


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DistributionChannel)
class DistributionChannelAdmin(admin.ModelAdmin):
    pass
