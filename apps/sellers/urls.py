from django.urls import path

from .views import SellersListCreateView, SellersRetrieveUpdateDestroyView

urlpatterns = [
    path('', SellersListCreateView.as_view()),

    path('/<int:pk>', SellersRetrieveUpdateDestroyView.as_view()),
]