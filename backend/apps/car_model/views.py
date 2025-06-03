from django.utils.decorators import method_decorator

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from drf_yasg.utils import swagger_auto_schema

from .filter import CarModelFilter
from .models import CarModelModel
from .permissions import IsAdminOrSuperUser
from .serializer import CarModelSerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        security=[]
    )
)
class CarModelListCreateView(ListCreateAPIView):
    """
        get:
            get car model list
        post:
            create new car model
    """

    queryset = CarModelModel.objects.all()
    serializer_class = CarModelSerializer
    filterset_class = CarModelFilter


    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminOrSuperUser()]
        return [AllowAny()]


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        security=[]
    )
)
class CarModelRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
        get:
            get car model detail by Id
        put:
            full update car model detail by Id
        patch:
            partial update car model detail by Id
        delete:
            delete car model detail by Id
    """

    queryset = CarModelModel.objects.all()
    serializer_class = CarModelSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminOrSuperUser()]
        return [AllowAny()]