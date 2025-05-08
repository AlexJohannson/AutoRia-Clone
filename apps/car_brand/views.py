from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from apps.car_brand.models import CarBrandModel
from apps.car_brand.permissions import IsAdminOrSuperUser
from apps.car_brand.serializer import CarBrandSerializer


class CarBrandListGreateView(ListCreateAPIView):
    queryset = CarBrandModel.objects.all()
    serializer_class = CarBrandSerializer

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