from django.contrib import admin

from .models import Debt


@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "category", "amount", "currency", "created_at", "updated_at")
    list_filter = ("user", "category", "currency")
    search_fields = ("user", "category", "currency")
