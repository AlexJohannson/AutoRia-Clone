from django.db import models

from core.models import BaseModel

from apps.sellers.models import SellersModel


class BaseAccountModel(BaseModel):
    class Meta:
        db_table = 'base_account'

    seller = models.OneToOneField(SellersModel, on_delete=models.CASCADE, related_name='base_account')
    account_type = models.CharField(max_length=10, default='base')
