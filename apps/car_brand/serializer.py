from rest_framework import serializers

from apps.car_brand.models import CarBrandModel


class CarBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBrandModel
        fields = ('id', 'brand')