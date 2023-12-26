from django.contrib import admin
from .models import OurServices


@admin.register(OurServices)
class OurServicesAdmin(admin.ModelAdmin):
    list_display = ["service", "is_user", "finished", "order_time", "finished_time", "user", "name", "email", "phone",
                    "message"]
    list_filter = ["service", "is_user", "finished", "order_time", "finished_time"]
    search_fields = ["name", "email", "phone", "message"]
    date_hierarchy = "order_time"
    ordering = ["order_time"]
