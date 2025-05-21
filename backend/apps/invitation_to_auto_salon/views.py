from rest_framework import status
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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

        return Response({'detail': 'Request approved and role assigned'}, status=status.HTTP_200_OK)



