from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, ReferralCode
from services.models import OurServices


@admin.register(ReferralCode)
class ReferralCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'user',)
    search_fields = ('code', 'user__username', 'user__email')


class ServicesInline(admin.TabularInline):
    model = OurServices
    extra = 0


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'is_staff', "email_confirmed", "referral_code", "score"]

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('address', 'phone', 'email_confirmed', "referral_code", "score")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": (
        "email",
        "username",
        "address",
        "phone",
        "email_confirmed",
        "referral_code",
        "is_staff",
        "score")}),)
    inlines = [ServicesInline]


admin.site.register(CustomUser, CustomUserAdmin)
