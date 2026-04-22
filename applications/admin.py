from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['worker', 'job', 'status', 'applied_at']
    list_filter = ['status']
    list_editable = ['status']
    search_fields = ['worker__username', 'job__title']
