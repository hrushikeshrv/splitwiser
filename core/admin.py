from django.contrib import admin
from core import models


@admin.register(models.TransactionGroup)
class TransactionGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "currency")


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("title", "amount", "date", "by", "group")


@admin.register(models.TransactionShare)
class TransactionShareAdmin(admin.ModelAdmin):
    list_display = ("transaction", "user", "amount_paid", "amount_owed")
