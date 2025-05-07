from rest_framework import serializers

from apps.base_account.models import BaseAccountModel
from apps.listings.serializer import ListingSerializer
from apps.sellers.models import SellersModel


class SellerSerializer(serializers.ModelSerializer):
    listings = ListingSerializer(many=True, read_only=True)
    account_type = serializers.SerializerMethodField()

    class Meta:
        model = SellersModel
        fields = (
            'id',
            'updated_at',
            'created_at',
            'listings',
            'account_type',
        )


    def get_account_type(self, obj):
        if hasattr(obj, 'premium_account'):
            return 'Premium'
        elif hasattr(obj, 'base_account'):
            return 'Base'

        return 'Unknown'


    def create(self, validated_data):
        user = self.context['request'].user
        validated_data.pop('user', None)
        seller = SellersModel.objects.create(user=user, **validated_data)
        BaseAccountModel.objects.create(seller=seller)

        return  seller

