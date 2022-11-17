from django.contrib import admin

from .models import Category, Expense


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["category", "amount", "currency", "description", "user"]
    list_filter = ["category", "user"]
