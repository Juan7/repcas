from django.contrib import admin

from . import models


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    pass


@admin.register(models.InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Quotation)
class QuotationAdmin(admin.ModelAdmin):
    pass


@admin.register(models.QuotationItem)
class QuotationItemAdmin(admin.ModelAdmin):
    pass
