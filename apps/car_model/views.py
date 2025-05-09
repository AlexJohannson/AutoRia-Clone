from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from .models import CarModelModel
from .permissions import IsAdminOrSuperUser
from .serializer import CarModelSerializer


class CarModelListCreateView(ListCreateAPIView):
    queryset = CarModelModel.objects.all()
    serializer_class = CarModelSerializer


    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminOrSuperUser()]
        return [AllowAny()]



class CarModelRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = CarModelModel.objects.all()
    serializer_class = CarModelSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminOrSuperUser()]
        return [AllowAny()]