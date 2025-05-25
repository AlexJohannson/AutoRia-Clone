from rest_framework import status
from rest_framework.generics import DestroyAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.tasks import (
    send_delete_invitation_email_task,
    send_join_request_approved_email_task,
    send_join_request_email_task,
)

from apps.invitation_to_auto_salon.models import JoinRequestModel
from apps.invitation_to_auto_salon.permissions import IsSalonAdminOrSuperUser
from apps.invitation_to_auto_salon.serializers import JoinRequestSerializer
from apps.salon_role.models import SalonRoleModels


class JoinRequestListCreateView(ListCreateAPIView):
    serializer_class = JoinRequestSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user


        if user.is_superuser or user.is_staff:
            return JoinRequestModel.objects.all()


        if hasattr(user, 'salon_role') and user.salon_role.role in ['superuser', 'admin']:
            return JoinRequestModel.objects.filter(auto_salon=user.salon_role.auto_salon)


        return JoinRequestModel.objects.filter(user=user)

    def perform_create(self, serializer):
        join_request = serializer.save(user=self.request.user, status='pending')

        send_join_request_email_task.delay(
            self.request.user.email,
            self.request.user.profile.name,
            join_request.role,
            join_request.auto_salon.name,
            join_request.auto_salon.location,
            created_at=str(join_request.created_at)
        )



class JoinRequestApproveApiView(UpdateAPIView):
    queryset = JoinRequestModel.objects.all()
    serializer_class = JoinRequestSerializer
    permission_classes = [IsAuthenticated, IsSalonAdminOrSuperUser]

    def update(self, request, *args, **kwargs):
        join_request = self.get_object()

        if join_request.status != 'pending':
            return Response({'detail': 'This request has already been processed'}, status=status.HTTP_400_BAD_REQUEST)

        if SalonRoleModels.is_role_taken(join_request.auto_salon, join_request.role):
            join_request.status = 'rejected'
            join_request.save()
            return Response({'detail': 'Role already taken. Request rejected'}, status=status.HTTP_400_BAD_REQUEST)


        SalonRoleModels.objects.create(
            user=join_request.user,
            auto_salon=join_request.auto_salon,
            role=join_request.role
        )



        join_request.status = 'approved'
        join_request.save()

        send_join_request_approved_email_task.delay(
            join_request.user.email,
            join_request.user.profile.name,
            join_request.auto_salon.name,
            join_request.auto_salon.location,
            updated_at=str(join_request.updated_at)
        )

        return Response({'detail': 'Request approved and role assigned'}, status=status.HTTP_200_OK)



class JoinRequestDeleteAPIView(DestroyAPIView):
    queryset = JoinRequestModel.objects.all()
    permission_classes = (IsSalonAdminOrSuperUser,)

    def destroy(self, request, *args, **kwargs):
        join_request = self.get_object()

        if join_request.status != 'pending':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        send_delete_invitation_email_task.delay(
            join_request.user.email,
            join_request.user.profile.name,
            join_request.auto_salon.name,
        )

        self.perform_destroy(join_request)

        return Response(status=status.HTTP_204_NO_CONTENT)



