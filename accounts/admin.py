from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'city', 'otp_verified', 'is_active']
    list_filter = ['role', 'otp_verified', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Kaamgar Info', {'fields': ('role', 'phone', 'city', 'bio', 'profile_photo', 'language', 'otp_verified')}),
    )
    search_fields = ['username', 'email', 'first_name', 'last_name']
