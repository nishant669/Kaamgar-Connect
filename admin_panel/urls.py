from django.urls import path
from . import views
app_name = 'admin_panel'
urlpatterns = [
    path('',                views.admin_dashboard,    name='dashboard'),
    path('users/',          views.manage_users,        name='users'),
    path('users/<int:pk>/toggle/', views.toggle_user, name='toggle_user'),
    path('jobs/',           views.manage_jobs,         name='jobs'),
    path('jobs/<int:pk>/feature/', views.toggle_job_featured, name='feature_job'),
    path('workers/<int:user_pk>/verify/', views.verify_worker, name='verify_worker'),
]
