from django.db import models

from core.models import BaseModel


class SellersModel(BaseModel):
    class Meta:
        db_table = 'sellers'

    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    age = models.IntegerField()
    male = models.CharField(max_length=100)

