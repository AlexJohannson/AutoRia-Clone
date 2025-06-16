from django.test import TestCase

from apps.car_brand.models import CarBrandModel
from apps.car_brand.serializer import CarBrandSerializer
from apps.car_model.models import CarModelModel


class CarBrandSerializerTest(TestCase):
    def setUp(self):
        self.car_brand = CarBrandModel.objects.create(brand="Toyota")

        self.car_model1 = CarModelModel.objects.create(car_model="Corolla", car_brand=self.car_brand)
        self.car_model2 = CarModelModel.objects.create(car_model="Camry", car_brand=self.car_brand)

    def test_car_brand_serialization(self):
        serializer = CarBrandSerializer(instance=self.car_brand)
        data = serializer.data

        self.assertEqual(data['id'], self.car_brand.id)
        self.assertEqual(data['brand'], self.car_brand.brand)

        self.assertIn('models', data)
        self.assertEqual(len(data['models']), 2)

        model_names = {model['car_model'] for model in data['models']}
        self.assertSetEqual(model_names, {"Corolla", "Camry"})

