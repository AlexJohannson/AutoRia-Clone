"""
ASGI config for configs project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from core.middlewares.socket_middleware import AuthSocketMiddleware

from .routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')



application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthSocketMiddleware(URLRouter(websocket_urlpatterns))
})
