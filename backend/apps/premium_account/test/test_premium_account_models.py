from django.db.utils import IntegrityError
from django.test import TestCase

from apps.auto_salon.models import AutoSalonModel
from apps.premium_account.models import PremiumAccountModel
from apps.sellers.models import SellersModel
from apps.user.models import UserModel


class PremiumAccountModelTestCase(TestCase):
    def setUp(self):

        self.user_seller = UserModel.objects.create(email="seller_user@example.com")

        self.user_auto_salon = UserModel.objects.create(email="auto_salon_user@example.com")


        self.seller = SellersModel.objects.create(user=self.user_seller)

        self.auto_salon = AutoSalonModel.objects.create(
            user=self.user_auto_salon,
            name="AutoShop",
            location="NYC"
        )

    def test_create_premium_account_for_seller(self):
        premium_account = PremiumAccountModel.objects.create(
            seller=self.seller,
            account_type="premium"
        )

        self.assertEqual(premium_account.seller, self.seller)
        self.assertEqual(premium_account.account_type, "premium")

    def test_create_premium_account_for_auto_salon(self):
        premium_account = PremiumAccountModel.objects.create(
            auto_salon=self.auto_salon,
            account_type="premium"
        )

        self.assertEqual(premium_account.auto_salon, self.auto_salon)
        self.assertEqual(premium_account.account_type, "premium")

    def test_only_one_account_per_seller(self):
        PremiumAccountModel.objects.create(
            seller=self.seller,
            account_type="premium"
        )

        with self.assertRaises(IntegrityError):
            PremiumAccountModel.objects.create(
                seller=self.seller,
                account_type="premium"
            )

    def test_only_one_account_per_auto_salon(self):
        PremiumAccountModel.objects.create(
            auto_salon=self.auto_salon,
            account_type="premium"
        )

        with self.assertRaises(IntegrityError):
            PremiumAccountModel.objects.create(
                auto_salon=self.auto_salon,
                account_type="premium"
            )