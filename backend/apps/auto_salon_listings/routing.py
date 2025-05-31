from django.urls import path

from apps.auto_salon_listings.consumer import AutoSalonListingConsumer

websocket_urlpatterns = [
    path('', AutoSalonListingConsumer.as_asgi()),
]