from django.db import models

class SellersModel(models.Model):
    class Meta:
        db_table = 'sellers'
    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    age = models.IntegerField()
    male = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
