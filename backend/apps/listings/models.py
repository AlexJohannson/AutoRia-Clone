import os

from django.db import models

from core.models import BaseModel
from core.services.file_service import upload_listing_photo

from apps.car_brand.models import CarBrandModel
from apps.car_model.models import CarModelModel
from apps.sellers.models import SellersModel


class ListingSellersModel(BaseModel):
    class Meta:
        db_table = 'listings'

    photo = models.ImageField(upload_to=upload_listing_photo, blank=True)
    brand = models.ForeignKey(CarBrandModel, on_delete=models.CASCADE, related_name='listings')
    car_model = models.ForeignKey(CarModelModel, on_delete=models.CASCADE, related_name='listings')
    year = models.IntegerField()
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    price = models.FloatField(null=True)
    currency = models.CharField(max_length=3, choices=[('USD', 'USD'), ('EUR', 'EUR'), ('UAH', 'UAH')], default='USD')
    price_usd = models.FloatField(null=True, blank=True)
    price_eur = models.FloatField(null=True, blank=True)
    price_uah = models.FloatField(null=True, blank=True)
    exchange_rate_used = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=250)
    seller = models.ForeignKey(SellersModel, on_delete=models.CASCADE, related_name='listings')
    is_active = models.BooleanField(default=True)
    avg_city_price = models.FloatField(null=True, blank=True)
    avg_region_price = models.FloatField(null=True, blank=True)
    avg_country_price = models.FloatField(null=True, blank=True)
    views = models.IntegerField(default=0)
    daily_views = models.IntegerField(default=0)
    weekly_views = models.IntegerField(default=0)
    monthly_views = models.IntegerField(default=0)
    last_view_date = models.DateField(null=True, blank=True)
    bad_word_attempts = models.IntegerField(default=0)


    def delete(self, *args, **kwargs):

        if self.photo:
            try:
                os.remove(self.photo.path)
            except Exception as e:
                print(f'Could not delete photo: {e}')
        super().delete(*args, **kwargs)