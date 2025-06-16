from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.sellers.models import SellersModel

UserModel = get_user_model()

class SellersModelTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(email='testuser@example.com', password='testpassword')

    def test_seller_creation(self):
        seller = SellersModel.objects.create(user=self.user)
        self.assertEqual(seller.user, self.user)
        self.assertTrue(seller.is_active)