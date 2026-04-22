from django.urls import path
from . import views
app_name = 'notifications'
urlpatterns = [
    path('', views.notification_list, name='list'),
    path('mark-read/', views.mark_all_read, name='mark_read'),
    path('count/', views.unread_count, name='count'),
]
