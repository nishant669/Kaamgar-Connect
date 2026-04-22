from django.urls import path
from . import views
app_name = 'applications'
urlpatterns = [
    path('',                views.my_applications, name='list'),
    path('apply/<int:job_pk>/', views.apply,       name='apply'),
    path('<int:pk>/withdraw/',  views.withdraw,     name='withdraw'),
]
