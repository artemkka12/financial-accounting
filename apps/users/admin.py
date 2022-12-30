from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ("first_name", "last_name", "email", "username", "password", "is_active", "is_staff")
    list_display = ("id", "username", "email", "first_name", "last_name", "is_active", "is_staff")
    search_fields = ("id", "email", "first_name", "last_name", "username")
