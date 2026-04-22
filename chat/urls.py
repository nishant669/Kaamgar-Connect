from django.urls import path
from . import views
app_name = 'chat'
urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('room/<int:pk>/', views.room, name='room'),
    path('start/<int:user_pk>/', views.start_chat, name='start'),
    path('room/<int:pk>/poll/', views.poll_messages, name='poll'),
]
