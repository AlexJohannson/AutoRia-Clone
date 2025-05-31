from django.urls import path

from channels.routing import URLRouter

from apps.auto_salon_listings.routing import websocket_urlpatterns as auto_salon_listings
from apps.chat.routing import websocket_urlpatterns as chat_routing
from apps.invitation_to_auto_salon.routing import websocket_urlpatterns as invitation_to_auto_salon
from apps.listings.routing import websocket_urlpatterns as listing_routing
from apps.salon_role.routing import websocket_urlpatterns as salon_role

websocket_urlpatterns = [
    path('api/chat/', URLRouter(chat_routing)),
    path('api/listings/', URLRouter(listing_routing)),
    path('api/auto_salon_listing/', URLRouter(auto_salon_listings)),
    path('api/salon_role/', URLRouter(salon_role)),
    path('api/invitation_to_auto_salon/', URLRouter(invitation_to_auto_salon)),
]
