from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.services.email_service import EmailService
from core.services.jwt_service import ActivateToken, JWTService, RecoveryToken, SocketToken

from apps.auth.serializers import EmailSerializers, PasswordSerializer, UserRoleSerializer
from apps.salon_role.models import SalonRoleModels
from apps.sellers.models import SellersModel
from apps.user.serializers import UserSerializer

UserModel = get_user_model()
class ActivateUserView(GenericAPIView):
    """
        patch:
            activate user view with activation token
    """

    permission_classes = (AllowAny,)

    def get_serializer(self):
        return None

    def patch(self, *args, **kwargs):
        token = kwargs['token']
        user = JWTService.verify_token(token, ActivateToken)
        user.is_active = True
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class RecoveryRequestView(GenericAPIView):
    """
        post:
            recovery request
    """

    permission_classes = (IsAuthenticated,)

    def get_serializer(self):
        return None

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = EmailSerializers(data=data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(UserModel, email=serializer.data['email'])
        EmailService.recovery(user)
        return Response({'Details': 'Link send to email'}, status.HTTP_200_OK)


class RecoveryPasswordView(GenericAPIView):
    """
        post:
            recovery password and get token
    """

    permission_classes = (IsAuthenticated,)

    def get_serializer(self):
        return None

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = PasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        token = kwargs['token']
        user = JWTService.verify_token(token, RecoveryToken)
        user.set_password(serializer.data['password'])
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)



class SocketTokenView(GenericAPIView):
    """
       get:
            get socket token
    """

    permission_classes = (IsAuthenticated,)

    def get_serializer(self):
        return None

    def get(self, *args, **kwargs):
        token = JWTService.create_token(user=self.request.user, token_class=SocketToken)
        return Response({'token': str(token)}, status.HTTP_200_OK)


class UserRoleView(GenericAPIView):
    """
        get:
            get site user role
    """

    permission_classes = [IsAuthenticated]

    def get_serializer(self):
        return None

    def get(self, request):
        user = request.user
        is_seller = SellersModel.objects.filter(user=user).exists()
        is_auto_salon_member = SalonRoleModels.objects.filter(user=user).exists()
        data = {
            'is_staff': user.is_staff,
            'is_user': user.is_active,
            'is_seller': is_seller,
            'is_auto_salon_member': is_auto_salon_member
        }
        serializer = UserRoleSerializer(instance=data)
        return Response(serializer.data)








