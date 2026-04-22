from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'employer', 'category', 'location', 'is_active', 'created_at']
    list_filter = ['category', 'job_type', 'is_active']
    search_fields = ['title', 'location', 'employer__username']
    list_editable = ['is_active']
