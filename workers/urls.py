from django.urls import path
from . import views
app_name = 'workers'
urlpatterns = [
    path('', views.worker_list, name='list'),
    path('<int:pk>/', views.worker_detail, name='detail'),
]
