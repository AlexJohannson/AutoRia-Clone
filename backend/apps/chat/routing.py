from django.urls import path

from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('<str:room>/', ChatConsumer.as_asgi())
]


