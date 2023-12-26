from django.contrib import admin
from .models import DiscountCode


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code',  'created_at')
    search_fields = ('user__username', 'code')
    list_filter = ('user',)
    ordering = ('created_at',)
