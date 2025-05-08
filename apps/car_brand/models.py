from django.db import models

from core.models import BaseModel


class CarBrandModel(BaseModel):
    class Meta:
        db_table = 'car_brand'

    brand = models.CharField(max_length=100)


