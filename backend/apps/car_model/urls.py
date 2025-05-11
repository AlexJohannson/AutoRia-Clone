from django.urls import path

from .views import CarModelListCreateView, CarModelRetrieveUpdateDestroyView

urlpatterns = [
    path('', CarModelListCreateView.as_view(), name='car_list_create'),
    path('/<int:pk>', CarModelRetrieveUpdateDestroyView.as_view(), name='car_detail_update'),
]