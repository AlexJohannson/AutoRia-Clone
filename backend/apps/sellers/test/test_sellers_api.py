from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase

from apps.base_account.models import BaseAccountModel
from apps.premium_account.models import PremiumAccountModel
from apps.sellers.models import SellersModel
from apps.user.models import ProfileModel

UserModel = get_user_model()


class SellersApiTestCase(APITestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(email='user@test.com', password='password')

        self.user.profile = ProfileModel.objects.create(
            user=self.user,
            name="Test",
            surname="Test",
            age=30,
            house=10,
            street="Main",
            city="Test",
            region="Test",
            country="Test",
            gender="Male"
        )
        self.user.save()

        self.admin = UserModel.objects.create_user(
            email='admin@test.com',
            password='password',
            is_staff=True,
            is_superuser=True
        )


        self.seller = SellersModel.objects.create(user=self.user)
        BaseAccountModel.objects.create(seller=self.seller)

    def test_get_sellers_list(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('sellers_list'))
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)

    def test_create_seller(self):
        new_user = UserModel.objects.create_user(email='newuser@test.com', password='password')
        new_user.profile = ProfileModel.objects.create(
            user=new_user,
            name="New",
            surname="New",
            age=25,
            house=5,
            street="New",
            city="New",
            region="New",
            country="New",
            gender="Male"
        )
        new_user.save()

        self.client.force_authenticate(user=new_user)
        response = self.client.post(reverse('sellers_list'), {})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(SellersModel.objects.filter(user=new_user).exists())

    def test_get_seller_by_id(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('sellers_detail', kwargs={'pk': self.seller.id}))
        self.assertEqual(response.status_code, 200)

    def test_delete_seller(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('sellers_detail', kwargs={'pk': self.seller.id}))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(SellersModel.objects.filter(id=self.seller.id).exists())

    def test_buy_premium_account(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('buy_premium'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(PremiumAccountModel.objects.filter(seller=self.seller).exists())