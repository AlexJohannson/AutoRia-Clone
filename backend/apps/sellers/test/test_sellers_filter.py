from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase

from apps.sellers.models import SellersModel
from apps.user.models import ProfileModel

UserModel = get_user_model()


class SellersFilterApiTestCase(APITestCase):
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

    def test_filter_seller_by_id(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('sellers_detail', kwargs={'pk': self.seller.id}), {'order': 'id'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.seller.id)