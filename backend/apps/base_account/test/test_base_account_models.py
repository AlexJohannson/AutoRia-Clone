from django.test import TestCase

from apps.base_account.models import BaseAccountModel
from apps.sellers.models import SellersModel
from apps.user.models import UserModel


class BaseAccountModelTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='testuser@example.com',
            password='testpassword123',
            is_active=True,
            is_staff=False,
            status='active',
        )

        self.seller = SellersModel.objects.create(
            user=self.user,
            is_active=True
        )

    def test_create_base_account(self):
        base_account = BaseAccountModel.objects.create(
            seller=self.seller,
            account_type='base'
        )
        self.assertEqual(base_account.seller, self.seller)
        self.assertEqual(base_account.account_type, 'base')

    def test_account_type_default(self):
        base_account = BaseAccountModel.objects.create(
            seller=self.seller
        )
        self.assertEqual(base_account.account_type, 'base')
