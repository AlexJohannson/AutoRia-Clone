from django.db import models

from apps.auto_salon.models import AutoSalonModel
from apps.user.models import UserModel


class SalonRoleModels(models.Model):
    class Meta:
        db_table = 'auto_salon_role'
    ROLE_CHOICES = [
        ('superuser', 'Superuser'),
        ('admin', 'Admin'),
        ('seller', 'Seller'),
        ('mechanic', 'Mechanic'),
    ]

    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='salon_role')
    auto_salon = models.ForeignKey(AutoSalonModel, on_delete=models.CASCADE, related_name='salon_role')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # def __str__(self):
    #     return f"{self.user.email} - {self.role} @ {self.auto_salon.name}"

    @classmethod
    def is_role_taken(cls, auto_salon, role):
        return cls.objects.filter(auto_salon=auto_salon, role=role).exists()


