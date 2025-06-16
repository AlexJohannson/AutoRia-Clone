from django.urls import path

from apps.invitation_to_auto_salon.consumer import JoinRequestConsumer

websocket_urlpatterns = [
    path('', JoinRequestConsumer.as_asgi(), name='join_request_websocket'),
]