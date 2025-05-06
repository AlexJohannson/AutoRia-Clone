from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .models import SellersModel
from .permissions import IsAdminOrSuperuser, IsSellerOrAdmin
from .serializers import SellerSerializer


class SellersListCreateView(ListCreateAPIView):
    queryset = SellersModel.objects.all()
    serializer_class = SellerSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [IsAdminOrSuperuser()]

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'sellers'):
            raise ValidationError("You are already a seller!")
        serializer.save()


class SellersRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = SellersModel.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsSellerOrAdmin]
    http_method_names = ['get', 'delete']

