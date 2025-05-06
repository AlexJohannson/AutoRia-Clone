from django.contrib.auth import get_user_model

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

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
