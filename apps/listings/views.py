from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import ListingSellersModel
from .permissions import IsOwnerOrAdmin
from .serializer import ListingSerializer


class ListingListCreateView(ListCreateAPIView):
    serializer_class = ListingSerializer

    def get_queryset(self):
        return ListingSellersModel.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

class ListingRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ListingSerializer
    permission_classes = [IsOwnerOrAdmin]
    http_method_names = ['get', 'put', 'delete']

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return ListingSellersModel.objects.all()
        return ListingSellersModel.objects.filter(seller__user=self.request.user)





