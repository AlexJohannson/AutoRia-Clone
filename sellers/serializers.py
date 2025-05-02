from rest_framework import serializers

from sellers.models import SellersModel


class SellerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=150)
    surname = serializers.CharField(max_length=150)
    age = serializers.IntegerField()
    male = serializers.CharField(max_length=100)
    status = serializers.BooleanField()

    def create(self, validated_data:dict):
        seller = SellersModel.objects.create(**validated_data)
        return seller

    def update(self, instance, validated_data:dict):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance



