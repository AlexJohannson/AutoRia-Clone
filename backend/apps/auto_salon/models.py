from django.db import models

from core.models import BaseModel

from apps.user.models import UserModel


class AutoSalonModel(BaseModel):
    class Meta:
        db_table = 'auto_salon'
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='auto_salon')


    def __str__(self):
        return f"{self.name} ({self.location})"
