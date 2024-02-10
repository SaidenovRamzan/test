from django.urls import path
from chat import views


urlpatterns = [
    path('chat/', views.get_chat, name='chat'),
    path('all_chat/', views.get_all_chats, name='all_chat'),
]
