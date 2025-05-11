from django.db import models

from core.models import BaseModel

from apps.car_brand.models import CarBrandModel


class CarModelModel(BaseModel):

    class Meta:
        db_table = 'car_model'


    car_model = models.CharField(max_length=100)
    car_brand = models.ForeignKey(CarBrandModel, on_delete=models.CASCADE, related_name='models',  null=False, blank=False)

