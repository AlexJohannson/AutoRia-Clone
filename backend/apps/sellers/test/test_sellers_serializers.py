from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIRequestFactory

from apps.base_account.models import BaseAccountModel
from apps.sellers.models import SellersModel
from apps.sellers.serializers import SellerSerializer
from apps.user.models import ProfileModel, UserModel


class SellerSerializerTestCase(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(email='user@test.com', password='password')

        self.user.profile = ProfileModel.objects.create(
            user=self.user,
            name="Test",
            surname="User",
            age=30,
            house=123,
            street="Main Street",
            city="TestCity",
            region="TestRegion",
            country="TestCountry",
            gender="Male"
        )

    def test_create_seller(self):
        factory = APIRequestFactory()
        request = factory.post(reverse('sellers_list'))
        request.user = self.user

        serializer = SellerSerializer(data={}, context={'request': request})
        self.assertTrue(serializer.is_valid(), serializer.errors)

        seller = serializer.save()

        self.assertEqual(seller.user, self.user)
        self.assertTrue(SellersModel.objects.filter(user=self.user).exists())
        self.assertTrue(BaseAccountModel.objects.filter(seller=seller).exists())

    def test_serializer_data(self):
        seller = SellersModel.objects.create(user=self.user)
        BaseAccountModel.objects.create(seller=seller)

        serializer = SellerSerializer(instance=seller)
        data = serializer.data

        self.assertEqual(data['user']['email'], self.user.email)
        self.assertEqual(data['account_type'], 'Base')
        self.assertEqual(data['listings'], [])
