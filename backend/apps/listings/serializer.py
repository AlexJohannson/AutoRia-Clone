from rest_framework import serializers

from ..car_brand.models import CarBrandModel
from ..car_model.models import CarModelModel
from ..car_model.serializer import CarModelSerializer
from .models import ListingSellersModel


class ListingSerializer(serializers.ModelSerializer):
    brand = serializers.SerializerMethodField()
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=CarBrandModel.objects.all(), write_only=True
    )

    car_model = CarModelSerializer(read_only=True)
    car_model_id = serializers.PrimaryKeyRelatedField(
        queryset=CarModelModel.objects.all(), write_only=True
    )


    class Meta:
        model = ListingSellersModel
        fields = (
            'id',
            'brand',
            'brand_id',
            'car_model',
            'car_model_id',
            'year',
            'country',
            'region',
            'city',
            'price',
            'seller',
            'views',
            'daily_views',
            'weekly_views',
            'monthly_views',
            'last_view_date'
        )

    def get_brand(self, obj):
        return obj.brand.brand if obj.brand else None



    def create(self, validated_data):
        validated_data['brand'] = validated_data.pop('brand_id')
        validated_data['car_model'] = validated_data.pop('car_model_id')
        return super().create(validated_data)