from django.urls import path

from apps.auto_salon.views import AutoSalonCreateApiView, AutoSalonRetrieveUpdateDestroyApiView

urlpatterns = [
    path('', AutoSalonCreateApiView.as_view(), name='auto_salon_create_list'),
    path('/<int:pk>', AutoSalonRetrieveUpdateDestroyApiView.as_view(), name='auto_salon_retrieve'),
]