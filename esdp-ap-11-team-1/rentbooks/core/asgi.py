"""
ASGI config for rentbooks project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import websocket_urlpatterns

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Создайте маршруты для WebSocket
websocket_application = ProtocolTypeRouter({
    "websocket": URLRouter(websocket_urlpatterns),
})

# Объедините HTTP и WebSocket приложения
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": websocket_application,
})

