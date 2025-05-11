from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..listings.models import ListingSellersModel
from ..sellers.models import SellersModel
from .permissions import IsAdminOrSuperuser, IsOwnerOrAdmin, IsSuperUserOnly
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


class UserBlockUnblockView(GenericAPIView):
    def patch(self, request, pk):
        user = get_object_or_404(UserModel, pk=pk)
        action = request.data.get('action')

        if action not in ['block', 'unblock']:
            return Response({'error': 'Invalid action. Use "block" or "unblock".'}, status=400)


        if action == 'block' and request.user == user and (user.is_staff or user.is_superuser):
            return Response({'error': 'Admin or superuser cannot block themselves.'}, status=403)


        user.is_active = action == 'unblock'
        user.status = 'active' if action == 'unblock' else 'blocked'
        user.save()

        seller = SellersModel.objects.filter(user=user).first()
        if seller:
            seller.is_active = user.is_active
            seller.save()
            ListingSellersModel.objects.filter(seller=seller).update(is_active=user.is_active)

        return Response({'message': f'User {user.profile.name} - {action}ed successfully', 'status': user.status})


class UserToAdminView(GenericAPIView):
    permission_classes = [IsSuperUserOnly]
    serializer_class = UserSerializer


    def patch(self, request, pk):
        user = get_object_or_404(UserModel, pk=pk)

        if user.is_staff:
            return Response({'detail': 'User is already an admin.'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_staff = True
        user.save()

        serializer = self.get_serializer(user)
        return Response({'message': f'User {user.profile.name} has been promoted to admin.',
                         'user': serializer.data},
                        status=status.HTTP_200_OK)
