from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.car_brand.models import CarBrandModel
from apps.car_model.models import CarModelModel


class CarModelFilterTest(APITestCase):
    def setUp(self):
        self.brand1 = CarBrandModel.objects.create(brand='Toyota')
        self.brand2 = CarBrandModel.objects.create(brand='Ford')
        self.brand3 = CarBrandModel.objects.create(brand='Honda')


        self.model1 = CarModelModel.objects.create(
            car_model='Camry',
            car_brand=self.brand1
        )
        self.model2 = CarModelModel.objects.create(
            car_model='Corolla',
            car_brand=self.brand1
        )
        self.model3 = CarModelModel.objects.create(
            car_model='Focus',
            car_brand=self.brand2
        )
        self.model4 = CarModelModel.objects.create(
            car_model='Civic',
            car_brand=self.brand3
        )

        self.list_url = reverse('car_list_create')

    def test_filter_car_models_by_brand_name(self):
        response = self.client.get(self.list_url, {'model': 'Toy'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)
        returned_models = [item['car_model'] for item in response.data['data']]
        self.assertIn('Camry', returned_models)
        self.assertIn('Corolla', returned_models)

    def test_filter_car_models_no_match(self):
        response = self.client.get(self.list_url, {'model': 'BMW'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 0)

    def test_ordering_car_models(self):
        response = self.client.get(self.list_url, {'order': 'car_model'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        car_models = [item['car_model'] for item in response.data['data']]
        self.assertEqual(car_models, sorted(car_models))
