from django.contrib import admin
from core import models


admin.site.register(models.TransactionGroup)
admin.site.register(models.Transaction)
admin.site.register(models.TransactionShare)
