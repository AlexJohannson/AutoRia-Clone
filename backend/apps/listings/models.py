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
    price = models.FloatField()
    description = models.CharField(max_length=250)
    seller = models.ForeignKey(SellersModel, on_delete=models.CASCADE, related_name='listings')
    is_active = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
    daily_views = models.IntegerField(default=0)
    weekly_views = models.IntegerField(default=0)
    monthly_views = models.IntegerField(default=0)
    last_view_date = models.DateField(null=True, blank=True)

    def delete(self, *args, **kwargs):

        if self.photo:
            try:
                os.remove(self.photo.path)
            except Exception as e:
                print(f'Could not delete photo: {e}')
        super().delete(*args, **kwargs)