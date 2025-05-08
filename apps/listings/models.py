from django.db import models

from core.models import BaseModel

from apps.car_brand.models import CarBrandModel
from apps.sellers.models import SellersModel


class ListingSellersModel(BaseModel):
    class Meta:
        db_table = 'listings'

    brand = models.ForeignKey(CarBrandModel, on_delete=models.CASCADE, related_name='listings')
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    price = models.FloatField()
    seller = models.ForeignKey(SellersModel, on_delete=models.CASCADE, related_name='listings')
    is_active = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
    daily_views = models.IntegerField(default=0)
    weekly_views = models.IntegerField(default=0)
    monthly_views = models.IntegerField(default=0)
    last_view_date = models.DateField(null=True, blank=True)