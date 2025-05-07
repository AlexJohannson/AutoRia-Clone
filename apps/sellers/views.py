from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..base_account.models import BaseAccountModel
from ..premium_account.models import PremiumAccountModel
from .models import SellersModel
from .permissions import IsAdminOrSuperuser, IsSellerOrAdmin
from .serializers import SellerSerializer


class SellersListCreateView(ListCreateAPIView):
    queryset = SellersModel.objects.filter(is_active=True)
    serializer_class = SellerSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [IsAdminOrSuperuser()]

    def perform_create(self, serializer):
        user = self.request.user

        if hasattr(user, 'sellers'):
            raise ValidationError("You are already a seller!")

        seller = serializer.save(user=user)

        if not hasattr(seller, 'base_account'):
            BaseAccountModel.objects.create(seller=seller)



class SellersRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = SellersModel.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsSellerOrAdmin]
    http_method_names = ['get', 'delete']



class PremiumAccountPurchaseApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        seller = SellersModel.objects.filter(user=request.user).first()

        if not seller:
            return Response({'error': 'You are not a seller'}, status=status.HTTP_400_BAD_REQUEST)

        if hasattr(seller, 'premium_account'):
            return Response({'error': 'You already have a premium account'}, status=status.HTTP_400_BAD_REQUEST)

        premium_account = PremiumAccountModel.objects.create(seller=seller)

        seller.base_account.delete()
        seller.premium_account = premium_account
        seller.save()

        return Response({'message': 'Premium account purchased successfully'}, status=status.HTTP_200_OK)
