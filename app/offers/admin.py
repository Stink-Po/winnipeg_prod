from django.contrib import admin
from .models import SiteOffers


@admin.register(SiteOffers)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "created_at", "availability",]
    list_filter = ["availability", "created_at",]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"
    ordering = ["availability", "created_at"]