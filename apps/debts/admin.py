from django.contrib import admin

from .models import Debt


# noinspection PyMethodMayBeStatic
@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "second_person",
        "amount",
        "type",
        "currency",
        "is_paid",
        "deadline",
        "partial_paid",
        "partial_paid_amount",
    ]
    list_filter = ["user", "second_person", "is_paid", "partial_paid"]
    search_fields = ["user", "second_person"]
    ordering = ["-created_at"]

    def currency(self, obj):
        return obj.user.currency
