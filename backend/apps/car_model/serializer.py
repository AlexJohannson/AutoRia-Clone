from rest_framework import serializers

from apps.car_brand.models import CarBrandModel
from apps.car_model.models import CarModelModel


class CarModelSerializer(serializers.ModelSerializer):
    car_brand = serializers.StringRelatedField(read_only=True)
    car_brand_id = serializers.PrimaryKeyRelatedField(
        queryset=CarBrandModel.objects.all(), write_only=True
    )

    class Meta:
        model = CarModelModel
        fields = ('id', 'car_model', 'car_brand', 'car_brand_id')

    def create(self, validated_data):
        validated_data['car_brand'] = validated_data.pop('car_brand_id')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'car_brand_id' in validated_data:
            instance.car_brand = validated_data.pop('car_brand_id')
        instance.car_model = validated_data.get('car_model', instance.car_model)
        instance.save()
        return instance