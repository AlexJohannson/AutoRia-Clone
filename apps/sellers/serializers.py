from rest_framework import serializers

from apps.sellers.models import SellersModel


class SellerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=150)
    surname = serializers.CharField(max_length=150)
    age = serializers.IntegerField()
    male = serializers.CharField(max_length=100)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


    def create(self, validated_data:dict):
        return SellersModel.objects.create(**validated_data)


    def update(self, instance, validated_data:dict):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance



