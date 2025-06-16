from django.test import TestCase

from apps.car_brand.models import CarBrandModel
from apps.car_model.models import CarModelModel
from apps.car_model.serializer import CarModelSerializer


class CarModelSerializerTest(TestCase):
    def setUp(self):
        self.brand = CarBrandModel.objects.create(brand='Toyota')

    def test_valid_data_serialization(self):
        data = {
            'car_model': 'Camry',
            'car_brand_id': self.brand.id
        }

        serializer = CarModelSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn('car_brand', serializer.validated_data)

    def test_invalid_data_serialization(self):
        data = {
            'car_model': 'Camry'
        }

        serializer = CarModelSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('car_brand_id', serializer.errors)

    def test_serializer_create(self):
        data = {
            'car_model': 'Corolla',
            'car_brand_id': self.brand.id
        }

        serializer = CarModelSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        car_model_instance = serializer.save()

        self.assertEqual(car_model_instance.car_model, 'Corolla')
        self.assertEqual(car_model_instance.car_brand, self.brand)

    def test_serializer_representation(self):
        car_model_instance = CarModelModel.objects.create(
            car_model='Yaris',
            car_brand=self.brand
        )

        serializer = CarModelSerializer(car_model_instance)
        data = serializer.data

        self.assertEqual(data['car_brand'], 'Toyota')
        self.assertEqual(data['car_model'], 'Yaris')
        self.assertNotIn('car_brand_id', data)
