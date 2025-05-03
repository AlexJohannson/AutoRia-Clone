from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from apps.listings.models import ListingSellersModel
from apps.listings.serializer import ListingSerializer


class ListingListCreateView(ListCreateAPIView):
    serializer_class = ListingSerializer
    queryset = ListingSellersModel.objects.all()



class ListingRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = ListingSellersModel.objects.all()
    serializer_class = ListingSerializer
    http_method_names = ['get', 'put', 'delete']





