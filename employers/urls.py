from django.urls import path
from . import views
app_name = 'employers'
urlpatterns = [
    path('', views.employer_list, name='list'),
    path('<int:pk>/', views.employer_detail, name='detail'),
]
