from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "message", "status"]
    list_filter = ["created", "status"]
    search_fields = ["name", "address"]
    date_hierarchy = "created"
    ordering = ["status", "created"]
