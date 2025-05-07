from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from ..listings.models import ListingSellersModel
from ..sellers.models import SellersModel
from .permissions import IsAdminOrSuperuser, IsOwnerOrAdmin
from .serializers import UserSerializer

UserModel = get_user_model()
class UserListCreateView(ListCreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAdminOrSuperuser()]


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAdmin]
    http_method_names = ['get', 'put', 'delete']




class UserBlockUnblockView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        user = get_object_or_404(UserModel, pk=pk)
        action = request.data.get('action')

        if action not in ['block', 'unblock']:
            return Response({'error': 'Invalid action. Use "block" or "unblock".'}, status=400)

        user.is_active = action == 'unblock'
        user.status = 'active' if action == 'unblock' else 'blocked'
        user.save()


        seller = SellersModel.objects.filter(user=user).first()
        if seller:
            seller.is_active = user.is_active
            seller.save()


            ListingSellersModel.objects.filter(seller=seller).update(is_active=user.is_active)

        return Response({'message': f'User {action}ed successfully', 'status': user.status})


