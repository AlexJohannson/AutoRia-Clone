from django.urls import path

from .views import PremiumAccountPurchaseApiView, SellersListCreateView, SellersRetrieveUpdateDestroyView

urlpatterns = [
    path('', SellersListCreateView.as_view(), name='sellers_list'),
    path('/<int:pk>', SellersRetrieveUpdateDestroyView.as_view(), name='sellers_detail'),
    path('/buy-premium', PremiumAccountPurchaseApiView.as_view(), name='buy_premium'),
]