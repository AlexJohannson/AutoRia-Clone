from django.db import models

from core.models import BaseModel

from apps.sellers.models import SellersModel


class PremiumAccountModel(BaseModel):
    class Meta:
        db_table = 'premium_account'

    seller = models.OneToOneField(SellersModel, on_delete=models.CASCADE, related_name='premium_account')
    account_type = models.CharField(max_length=10, default='premium')
