from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.car_brand.models import CarBrandModel
from apps.user.models import UserModel


class CarBrandAPITest(APITestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='user@example.com',
            password='testpassword',
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


        self.brand1 = CarBrandModel.objects.create(brand='Toyota')
        self.brand2 = CarBrandModel.objects.create(brand='Ford')

        self.list_url = reverse('car_brand_list')
        self.detail_url = lambda pk: reverse('car_brand_retrieve', args=[pk])


    def test_get_car_brand_list_anyone(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)

    def test_post_car_brand_unauthenticated_unauthorized(self):
        data = {'brand': 'Honda'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_car_brand_as_admin_success(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'brand': 'Honda'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['brand'], 'Honda')

    def test_get_car_brand_detail_anyone(self):
        url = self.detail_url(self.brand1.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['brand'], 'Toyota')

    def test_put_car_brand_unauthenticated_unauthorized(self):
        url = self.detail_url(self.brand1.pk)
        data = {'brand': 'UpdatedBrand'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_car_brand_as_admin_success(self):
        self.client.force_authenticate(user=self.admin_user)
        url = self.detail_url(self.brand1.pk)
        data = {'brand': 'UpdatedBrand'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['brand'], 'UpdatedBrand')

    def test_patch_car_brand_as_admin_success(self):
        self.client.force_authenticate(user=self.admin_user)
        url = self.detail_url(self.brand2.pk)
        data = {'brand': 'PartialUpdateBrand'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['brand'], 'PartialUpdateBrand')

    def test_delete_car_brand_as_admin_success(self):
        self.client.force_authenticate(user=self.admin_user)
        url = self.detail_url(self.brand2.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CarBrandModel.objects.filter(pk=self.brand2.pk).exists())

    def test_delete_car_brand_unauthenticated_unauthorized(self):
        url = self.detail_url(self.brand1.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

