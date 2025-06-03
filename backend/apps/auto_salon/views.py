from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.tasks import send_delete_auto_salon_task
from core.tasks.send_auto_salon_create_email_task import send_auto_salon_create_email_task

from apps.auto_salon.filter import AutoSalonFilter
from apps.auto_salon.models import AutoSalonModel
from apps.auto_salon.permissions import IsAdminOrSuperUser, IsSalonOwnerAdminOrSuperuser
from apps.auto_salon.serializers import AutoSalonSerializer
from apps.premium_account.models import PremiumAccountModel
from apps.salon_role.models import SalonRoleModels


class AutoSalonCreateApiView(ListCreateAPIView):
    """
        get:
            get auto salon list
        post:
            create new auto salon
    """

    queryset = AutoSalonModel.objects.all()
    serializer_class = AutoSalonSerializer
    filterset_class = AutoSalonFilter


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
    """
        get:
            get auto salon by Id
        put:
           full upgrade auto salon by Id
        delete:
            delete auto salon by Id
    """

    queryset = AutoSalonModel.objects.all()
    serializer_class = AutoSalonSerializer
    permission_classes = (IsSalonOwnerAdminOrSuperuser, )
    http_method_names = ['get', 'put', 'delete']

    def destroy(self, request, *args, **kwargs):
        auto_salon = self.get_object()
        send_delete_auto_salon_task.delay(
            auto_salon.user.email,
            auto_salon.user.profile.name,
            auto_salon.name,
            auto_salon.location
        )
        self.perform_destroy(auto_salon)
        return Response(status=status.HTTP_204_NO_CONTENT)

