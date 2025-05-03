from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from apps.sellers.models import SellersModel
from apps.sellers.serializers import SellerSerializer


class SellersListCreateView(ListCreateAPIView):
    queryset = SellersModel.objects.all()
    serializer_class = SellerSerializer



class SellersRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = SellersModel.objects.all()
    serializer_class = SellerSerializer
    http_method_names = ['get', 'put', 'delete']

