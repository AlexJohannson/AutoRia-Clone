from django.urls import path

from apps.salon_role.views import SalonRoleListApiView, SalonRoleRetrieveDestroyAPIView

urlpatterns = [
    path('', SalonRoleListApiView.as_view(), name='salon_role_list'),
    path('/<int:pk>', SalonRoleRetrieveDestroyAPIView.as_view(), name='salon_role_retrieve'),
]