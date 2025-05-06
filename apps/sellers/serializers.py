from rest_framework import serializers

from apps.listings.serializer import ListingSerializer
from apps.sellers.models import SellersModel


class SellerSerializer(serializers.ModelSerializer):
    listings = ListingSerializer(many=True, read_only=True)
    class Meta:
        model = SellersModel
        fields = (
            'id',
            'updated_at',
            'created_at',
            'listings'
        )

    def create(self, validated_data):
        user = self.context['request'].user
        return SellersModel.objects.create(user=user, **validated_data)


