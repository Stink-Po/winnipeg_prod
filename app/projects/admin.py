from django.contrib import admin
from .models import OurProjects


@admin.register(OurProjects)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "completed_at"]
    list_filter = ["title", "completed_at"]
    search_fields = ["title", ]
    date_hierarchy = "completed_at"
    ordering = ["completed_at"]
