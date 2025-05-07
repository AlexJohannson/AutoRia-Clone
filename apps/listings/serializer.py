from rest_framework import serializers

from .models import ListingSellersModel


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingSellersModel
        fields = (
            'id',
            'brand',
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