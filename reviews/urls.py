from django.urls import path
from . import views
app_name = 'reviews'
urlpatterns = [
    path('leave/<int:user_pk>/', views.leave_review, name='leave'),
]
