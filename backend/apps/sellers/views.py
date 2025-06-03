from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.tasks.send_premium_activate_email_task import send_premium_activate_email_task
from core.tasks.send_seller_create_email_task import send_seller_create_email_task
from core.tasks.send_seller_deleted_email_task import send_seller_deleted_email_task

from ..base_account.models import BaseAccountModel
from ..premium_account.models import PremiumAccountModel
from .filter import SellerFilter
from .models import SellersModel
from .permissions import IsAdminOrSuperuser, IsSellerOrAdmin
from .serializers import SellerSerializer


class SellersListCreateView(ListCreateAPIView):
    """
        get:
            get all sellers list
        post:
            create new seller
    """

    queryset = SellersModel.objects.filter(is_active=True)
    serializer_class = SellerSerializer
    filterset_class = SellerFilter

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

        send_seller_create_email_task.delay(user.email, user.profile.name)



class SellersRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
        get:
            get seller details by id
        delete:
            delete seller by id
    """

    queryset = SellersModel.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsSellerOrAdmin]
    http_method_names = ['get', 'delete']

    def delete(self, request, *args, **kwargs):
        seller = self.get_object()
        email = seller.user.email
        name = seller.user.profile.name

        send_seller_deleted_email_task.delay(email, name)

        self.perform_destroy(seller)
        return Response(status=status.HTTP_204_NO_CONTENT)



class PremiumAccountPurchaseApiView(GenericAPIView):
    """
        post:
            buy premium account for sellers
    """

    permission_classes = [IsAuthenticated]

    def get_serializer(self):
        return None

    def post(self, request, *args, **kwargs):
        seller = SellersModel.objects.filter(user=request.user).first()

        if not seller:
            return Response({'error': 'You are not a seller'}, status=status.HTTP_400_BAD_REQUEST)

        if hasattr(seller, 'premium_account'):
            return Response({'error': 'You already have a premium account'}, status=status.HTTP_400_BAD_REQUEST)

        premium_account = PremiumAccountModel.objects.create(seller=seller)
        send_premium_activate_email_task(seller.user.email, seller.user.profile.name)

        seller.base_account.delete()
        seller.premium_account = premium_account
        seller.save()

        return Response({'message': 'Premium account purchased successfully'}, status=status.HTTP_200_OK)
