from django.test import TestCase

from apps.car_brand.models import CarBrandModel
from apps.user.models import UserModel


class CarBrandModelTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='testuser@example.com',
            password='testpassword123',
            is_active=True,
            is_staff=True,
            status='active',
        )

    def test_create_car_brand(self):
        brand_name = "Toyota"
        car_brand = CarBrandModel.objects.create(brand=brand_name)

        self.assertEqual(car_brand.brand, brand_name)
        self.assertEqual(str(car_brand), brand_name)
