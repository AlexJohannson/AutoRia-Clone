from rest_framework import serializers

from apps.car_brand.models import CarBrandModel
from apps.car_model.serializer import CarModelSerializer


class CarBrandSerializer(serializers.ModelSerializer):
    models = CarModelSerializer(read_only=True, many=True)

    class Meta:
        model = CarBrandModel
        fields = ('id', 'brand', 'models')




