from django.db import models

from core.models import BaseModel

from apps.user.models import UserModel


class SellersModel(BaseModel):
    class Meta:
        db_table = 'sellers'

    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='sellers')


