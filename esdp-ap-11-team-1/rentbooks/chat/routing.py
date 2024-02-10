# myapp/routing.py
from django.urls import re_path

from chat import consumers

# chat/routing.py
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<sender_id>\d+)/(?P<recipient_id>\d+)/(?P<user_shelf_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]
