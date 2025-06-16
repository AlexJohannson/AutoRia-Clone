from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.car_brand.models import CarBrandModel
from apps.car_model.models import CarModelModel
from apps.user.models import UserModel


class CarModelAPITest(APITestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='user@example.com',
            password='password123',
            is_active=True,
            is_staff=False,
            status='active',
        )

        self.admin_user = UserModel.objects.create_user(
            email='admin@example.com',
            password='adminpassword',
            is_active=True,
            is_staff=True,
            status='active',
        )


        self.brand = CarBrandModel.objects.create(brand='Toyota')
        self.car1 = CarModelModel.objects.create(
            car_model='Camry',
            car_brand=self.brand
        )
        self.car2 = CarModelModel.objects.create(
            car_model='Corolla',
            car_brand=self.brand
        )


        self.list_url = reverse('car_list_create')
        self.detail_url = lambda pk: reverse('car_detail_update', args=[pk])


    def test_get_car_model_list_anyone(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(item['car_model'] == 'Camry' for item in response.data['data']))
        self.assertTrue(any(item['car_model'] == 'Corolla' for item in response.data['data']))


    def test_post_car_model_unauthenticated_forbidden(self):
        data = {'car_model': 'RAV4', 'car_brand_id': self.brand.id}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_car_model_as_non_admin_forbidden(self):
        self.client.force_authenticate(user=self.user)
        data = {'car_model': 'RAV4', 'car_brand_id': self.brand.id}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_car_model_as_admin_success(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'car_model': 'RAV4', 'car_brand_id': self.brand.id}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['car_model'], 'RAV4')


    def test_get_car_model_detail_anyone(self):
        url = self.detail_url(self.car1.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['car_model'], 'Camry')


    def test_put_car_model_unauthenticated_forbidden(self):
        url = self.detail_url(self.car1.pk)
        data = {'car_model': 'Camry Updated', 'car_brand_id': self.brand.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_car_model_as_non_admin_forbidden(self):
        self.client.force_authenticate(user=self.user)
        url = self.detail_url(self.car1.pk)
        data = {'car_model': 'Camry Updated', 'car_brand_id': self.brand.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_car_model_as_admin_success(self):
        car_brand = CarBrandModel.objects.create(brand="Toyota")

        car_model = CarModelModel.objects.create(
            car_model="OldName",
            car_brand=car_brand
        )

        url = reverse(
            'car_detail_update',
            kwargs={'pk': car_model.pk}
        )

        data = {
            'car_model': 'NewName',
            'car_brand_id': car_brand.id
        }

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['car_model'], 'NewName')
        self.assertEqual(response.data['car_brand'], str(car_brand))

        car_model.refresh_from_db()
        self.assertEqual(car_model.car_model, 'NewName')
        self.assertEqual(car_model.car_brand, car_brand)


    def test_patch_car_model_as_admin_success(self):
        self.client.force_authenticate(user=self.admin_user)
        url = self.detail_url(self.car2.pk)
        data = {'car_model': 'Corolla Partial'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['car_model'], 'Corolla Partial')


    def test_delete_car_model_unauthenticated_forbidden(self):
        url = self.detail_url(self.car1.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_car_model_as_non_admin_forbidden(self):
        self.client.force_authenticate(user=self.user)
        url = self.detail_url(self.car1.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_car_model_as_admin_success(self):
        self.client.force_authenticate(user=self.admin_user)
        url = self.detail_url(self.car1.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CarModelModel.objects.filter(pk=self.car1.pk).exists())
