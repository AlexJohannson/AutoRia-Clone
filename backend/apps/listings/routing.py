from django.urls import path

from .consumer import ListingConsumer

websocket_urlpatterns = [
    path('', ListingConsumer.as_asgi(), name='listings_websocket'),
]