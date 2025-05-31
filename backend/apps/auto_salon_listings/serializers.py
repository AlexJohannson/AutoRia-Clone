from django.db.models import Avg

from rest_framework import serializers

from apps.auto_salon_listings.models import AutoSalonListingModel
from apps.car_brand.models import CarBrandModel
from apps.car_model.models import CarModelModel
from apps.car_model.serializer import CarModelSerializer


class AutoSalonListingSerializer(serializers.ModelSerializer):
    brand = serializers.SerializerMethodField()
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=CarBrandModel.objects.all(),
        write_only=True,
    )

    car_model = CarModelSerializer(read_only=True)
    car_model_id = serializers.PrimaryKeyRelatedField(
        queryset=CarModelModel.objects.all(),
        write_only=True,
    )

    views = serializers.IntegerField(read_only=True)
    daily_views = serializers.IntegerField(read_only=True)
    weekly_views = serializers.IntegerField(read_only=True)
    monthly_views = serializers.IntegerField(read_only=True)
    last_view_date = serializers.DateTimeField(read_only=True)
    price = serializers.FloatField()
    avg_city_price = serializers.FloatField(read_only=True)
    avg_region_price = serializers.FloatField(read_only=True)
    avg_country_price = serializers.FloatField(read_only=True)

    class Meta:
        model = AutoSalonListingModel
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
            'currency',
            'price_usd',
            'price_eur',
            'price_uah',
            'exchange_rate_used',
            'description',
            'auto_salon',
            'photo',
            'views',
            'daily_views',
            'weekly_views',
            'monthly_views',
            'last_view_date',
            'avg_city_price',
            'avg_region_price',
            'avg_country_price',
            'is_active',
            'bad_word_attempts',
        )
    def get_brand(self, obj):
        return obj.brand.brand if obj.brand else None

    def create(self, validated_data):
        validated_data['brand'] = validated_data.pop('brand_id')
        validated_data['car_model'] = validated_data.pop('car_model_id')
        return super().create(validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if not request:
            return data


        is_premium = hasattr(instance.auto_salon, 'premium_account')

        if not is_premium:

            for field in [
                'views', 'daily_views', 'weekly_views', 'monthly_views',
                'last_view_date', 'avg_city_price', 'avg_region_price', 'avg_country_price'
            ]:
                data.pop(field, None)
        else:

            avg_city_price = AutoSalonListingModel.objects.filter(
                city=instance.city, is_active=True
            ).aggregate(Avg('price'))['price__avg']
            avg_region_price = AutoSalonListingModel.objects.filter(
                region=instance.region, is_active=True
            ).aggregate(Avg('price'))['price__avg']
            avg_country_price = AutoSalonListingModel.objects.filter(
                country=instance.country, is_active=True
            ).aggregate(Avg('price'))['price__avg']

            data.update({
                'avg_city_price': round(avg_city_price, 2) if avg_city_price else 0.0,
                'avg_region_price': round(avg_region_price, 2) if avg_region_price else 0.0,
                'avg_country_price': round(avg_country_price, 2) if avg_country_price else 0.0,
            })

        return data

    def update(self, instance, validated_data):
        if 'brand_id' in validated_data:
            validated_data['brand'] = validated_data.pop('brand_id')
        if 'car_model_id' in validated_data:
            validated_data['car_model'] = validated_data.pop('car_model_id')
        return super().update(instance, validated_data)

    def validate_price(self, price):
        if price <= 0:
            raise serializers.ValidationError('Price must be greater than 0')
        return price



class AutoSalonListingPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoSalonListingModel
        fields = ('photo',)


