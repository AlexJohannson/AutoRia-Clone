from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from core.tasks import send_role_deleted_email_task

from apps.salon_role.filetr import SalonRoleFilter
from apps.salon_role.models import SalonRoleModels
from apps.salon_role.permissions import CanManageSalonRole, IsSalonMemberOrAdmin
from apps.salon_role.serializers import SalonRoleSerializer


class SalonRoleListApiView(ListAPIView):
    queryset = SalonRoleModels.objects.all()
    serializer_class = SalonRoleSerializer
    permission_classes = (IsSalonMemberOrAdmin,)
    filterset_class = SalonRoleFilter



class SalonRoleRetrieveDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = SalonRoleModels.objects.all()
    serializer_class = SalonRoleSerializer
    permission_classes = (IsSalonMemberOrAdmin, CanManageSalonRole)
    http_method_names = ['get', 'post', 'delete']


    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        send_role_deleted_email_task.delay(
            instance.user.email,
            instance.user.profile.name,
            instance.auto_salon.name,
            instance.role
        )


        if request.user == instance.user:

            if instance.role == 'superuser':
                auto_salon = instance.auto_salon
                auto_salon.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)


            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)


        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


