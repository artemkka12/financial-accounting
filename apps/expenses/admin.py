from django.contrib import admin

from .models import Attachment, Category, Expense


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["pk", "name"]


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["pk", "category", "amount", "currency", "description", "user"]
    list_filter = ["category", "user"]


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ["pk", "user", "file"]
    list_filter = ["user"]
