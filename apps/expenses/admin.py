from django.contrib import admin

from .models import Category, Expense


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "user"]
    search_fields = ["name", "user__username"]
    list_filter = ["user"]


# noinspection PyMethodMayBeStatic
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["pk",  "user", "category", "amount", "date", "description"]
    list_filter = ["category", "user"]

    def date(self, obj):
        return obj.created_at.date()

