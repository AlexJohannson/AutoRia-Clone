from django.urls import path

from apps.salon_role.consumer import SalonRoleConsumer

websocket_urlpatterns = [
    path('', SalonRoleConsumer.as_asgi(), name='salon_role_consumer'),
]