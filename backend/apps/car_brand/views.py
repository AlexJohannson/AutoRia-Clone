from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from .filter import CarBrandFilter
from .models import CarBrandModel
from .permissions import IsAdminOrSuperUser
from .serializer import CarBrandSerializer


class CarBrandListGreateView(ListCreateAPIView):
    queryset = CarBrandModel.objects.all()
    serializer_class = CarBrandSerializer
    filterset_class = CarBrandFilter

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminOrSuperUser()]
        return [AllowAny()]


class CarBrandRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = CarBrandModel.objects.all()
    serializer_class = CarBrandSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminOrSuperUser()]
        return [AllowAny()]