from django.contrib import admin

from . import models


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['number']
    raw_id_fields = ['client']


@admin.register(models.InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    raw_id_fields = ['invoice']


@admin.register(models.Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ['number']
    raw_id_fields = ['client']


@admin.register(models.QuotationItem)
class QuotationItemAdmin(admin.ModelAdmin):
    raw_id_fields = ['quotation']
