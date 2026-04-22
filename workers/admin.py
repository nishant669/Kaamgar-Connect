from django.contrib import admin
from .models import WorkerProfile

@admin.register(WorkerProfile)
class WorkerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'skills', 'experience_years', 'daily_rate', 'availability', 'rating', 'aadhar_verified']
    list_filter = ['skills', 'availability', 'aadhar_verified']
    search_fields = ['user__username', 'user__first_name']
