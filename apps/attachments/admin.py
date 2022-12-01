from django.contrib import admin

from .models import Attachment


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ["id", "file", "user", "created_at", "updated_at"]
    list_display_links = ["id", "file", "user"]
    list_filter = ["user"]
    search_fields = ["file", "user"]
