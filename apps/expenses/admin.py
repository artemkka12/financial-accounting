from django.contrib import admin
from models import Category, Expense


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "user"]
    search_fields = ["name", "user__username"]
    list_filter = ["user"]


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["pk", "category", "amount", "currency", "description", "user"]
    list_filter = ["category", "user"]
