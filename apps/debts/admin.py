from django.contrib import admin

from .models import Debt


@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "person",
        "second_person",
        "amount",
        "currency",
        "type",
        "is_paid",
        "deadline",
        "partial_paid",
        "partial_paid_amount",
    ]
    list_filter = ["person", "second_person", "is_paid", "partial_paid"]
    search_fields = ["person", "second_person"]
    ordering = ["-created_at"]
