from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.tasks.send_auto_salon_create_email_task import send_auto_salon_create_email_task

from apps.auto_salon.models import AutoSalonModel
from apps.auto_salon.permissions import IsAdminOrSuperUser, IsSalonOwnerAdminOrSuperuser
from apps.auto_salon.serializers import AutoSalonSerializer
from apps.premium_account.models import PremiumAccountModel
from apps.salon_role.models import SalonRoleModels


class AutoSalonCreateApiView(ListCreateAPIView):
    queryset = AutoSalonModel.objects.all()
    serializer_class = AutoSalonSerializer


    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [IsAdminOrSuperUser()]

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'auto_salon'):
            raise ValidationError("You already own an auto salon.")

        auto_salon = serializer.save(user=self.request.user)

        SalonRoleModels.objects.create(
            user = self.request.user,
            auto_salon = auto_salon,
            role = 'superuser',
        )
        PremiumAccountModel.objects.create(auto_salon=auto_salon)
        send_auto_salon_create_email_task.delay(
            auto_salon.user.email,
            auto_salon.user.profile.name,
            auto_salon.name,
            auto_salon.location

        )


class AutoSalonRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    queryset = AutoSalonModel.objects.all()
    serializer_class = AutoSalonSerializer
    permission_classes = (IsSalonOwnerAdminOrSuperuser, )
    http_method_names = ['get', 'put', 'delete']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

