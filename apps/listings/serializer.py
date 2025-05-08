# from rest_framework import serializers
#
# from ..car_brand.models import CarBrandModel
# from ..car_brand.serializer import CarBrandSerializer
# from .models import ListingSellersModel
#
#
# class ListingSerializer(serializers.ModelSerializer):
#     brand = CarBrandSerializer(read_only=True)
#
#
#
#     class Meta:
#         model = ListingSellersModel
#         fields = (
#             'id',
#             'brand',
#             'model',
#             'year',
#             'country',
#             'region',
#             'city',
#             'price',
#             'seller',
#             'views',
#             'daily_views',
#             'weekly_views',
#             'monthly_views',
#             'last_view_date'
#         )


from rest_framework import serializers

from ..car_brand.models import CarBrandModel
from ..car_brand.serializer import CarBrandSerializer
from .models import ListingSellersModel


class ListingSerializer(serializers.ModelSerializer):
    brand = CarBrandSerializer(read_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=CarBrandModel.objects.all(), write_only=True
    )

    class Meta:
        model = ListingSellersModel
        fields = (
            'id',
            'brand',
            'brand_id',
            'model',
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

    def create(self, validated_data):
        brand = validated_data.pop('brand_id')
        validated_data['brand'] = brand
        return super().create(validated_data)
