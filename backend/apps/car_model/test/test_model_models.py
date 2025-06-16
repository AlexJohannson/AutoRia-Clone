from django.test import TestCase

from apps.car_brand.models import CarBrandModel
from apps.car_model.models import CarModelModel


class CarModelModelTest(TestCase):
    def setUp(self):
        self.brand = CarBrandModel.objects.create(brand='Toyota')

    def test_create_car_model(self):
        car_model = CarModelModel.objects.create(
            car_model='Camry',
            car_brand=self.brand
        )

        self.assertEqual(CarModelModel.objects.count(), 1)

        self.assertEqual(car_model.car_model, 'Camry')
        self.assertEqual(car_model.car_brand, self.brand)
        self.assertEqual(str(car_model.car_brand), 'Toyota')

    def test_car_model_brand_relation(self):
        car_model = CarModelModel.objects.create(
            car_model='Corolla',
            car_brand=self.brand
        )
        self.assertIn(car_model, self.brand.models.all())

    def test_multiple_car_models_for_one_brand(self):
        model1 = CarModelModel.objects.create(
            car_model='Camry',
            car_brand=self.brand
        )
        model2 = CarModelModel.objects.create(
            car_model='Corolla',
            car_brand=self.brand
        )

        self.assertEqual(self.brand.models.count(), 2)
        self.assertIn(model1, self.brand.models.all())
        self.assertIn(model2, self.brand.models.all())
