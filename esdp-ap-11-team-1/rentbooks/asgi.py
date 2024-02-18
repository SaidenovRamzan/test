import os
import sys
import asyncio
import importlib

from django.core.asgi import get_asgi_application
from channels.layers import get_channel_layer
from django.core.handlers.asgi import ASGIHandler
from django.conf import settings
from channels.routing import ProtocolTypeRouter, URLRouter
from django.contrib.staticfiles.handlers import StaticFilesHandler

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rentbooks.core.settings")
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

django_asgi_app = get_asgi_application()
channel_layer = get_channel_layer()


async def application(scope, receive, send):
    if scope["type"] == "http":
        await django_asgi_app(scope, receive, send)
    elif scope["type"] == "websocket.connect":
        # Handle WebSocket connections here
        pass
    elif scope["type"] == "websocket.disconnect":
        # Handle WebSocket disconnections here
        pass
    # Add more scop
