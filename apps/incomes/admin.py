from django.contrib import admin

from .models import Income


# noinspection PyMethodMayBeStatic
@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ["pk", "amount", "currency", "description", "user"]
    list_filter = ["user"]

    def currency(self, obj):
        return obj.user.currency
