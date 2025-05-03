from rest_framework import serializers

from apps.listings.serializer import ListingSerializer
from apps.sellers.models import SellersModel


class SellerSerializer(serializers.ModelSerializer):
    listings = ListingSerializer(many=True, read_only=True)
    class Meta:
        model = SellersModel
        fields = ('id', 'name', 'surname', 'age', 'male', 'updated_at', 'created_at', 'listings')


