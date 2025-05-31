from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators as V
from django.db import models

from core.enums.regex_enum import RegexEnum
from core.models import BaseModel

from .managers import UserManager


class UserModel(AbstractBaseUser, PermissionsMixin, BaseModel):
    class Meta:
        db_table = 'auth_user'

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    status = models.CharField(max_length=10,
                              choices=[
                                  ('active', 'Active'),
                                  ('blocked', 'Blocked')],
                              default='active'
                              )

    USERNAME_FIELD = 'email'

    objects = UserManager()


class ProfileModel(BaseModel):
    class Meta:
        db_table = 'profile'

    name = models.CharField(max_length=20, validators=[V.RegexValidator(RegexEnum.NAME.pattern, RegexEnum.NAME.msg)])
    surname = models.CharField(max_length=20, validators=[V.RegexValidator(RegexEnum.SURNAME.pattern, RegexEnum.SURNAME.msg)])
    age = models.IntegerField(validators=[V.MinValueValidator(18)])
    house = models.IntegerField()
    street = models.CharField(max_length=30, validators=[V.RegexValidator(RegexEnum.STREET.pattern, RegexEnum.STREET.msg)])
    city = models.CharField(max_length=30, validators=[V.RegexValidator(RegexEnum.CITY.pattern, RegexEnum.CITY.msg)])
    region = models.CharField(max_length=30, validators=[V.RegexValidator(RegexEnum.REGION.pattern, RegexEnum.REGION.msg)])
    country = models.CharField(max_length=30, validators=[V.RegexValidator(RegexEnum.COUNTRY.pattern, RegexEnum.COUNTRY.msg)])
    gender = models.CharField(max_length=10, validators=[V.RegexValidator(RegexEnum.GENDER.pattern, RegexEnum.GENDER.msg)])
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='profile')


