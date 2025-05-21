from django.db import models

from core.models import BaseModel

from apps.auto_salon.models import AutoSalonModel
from apps.user.models import UserModel


class JoinRequestModel(BaseModel):
    class Meta:
        db_table = 'invitation_to_auto_salon'
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('seller', 'Seller'),
        ('mechanic', 'Mechanic'),
    ]

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='join_request')
    auto_salon = models.ForeignKey(AutoSalonModel, on_delete=models.CASCADE, related_name='join_request')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='pending')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)


