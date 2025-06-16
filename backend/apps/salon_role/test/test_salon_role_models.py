from django.test import TestCase

from apps.auto_salon.models import AutoSalonModel
from apps.salon_role.models import SalonRoleModels
from apps.user.models import UserModel


class SalonRoleModelsTestCase(TestCase):
    def setUp(self):
        self.owner = UserModel.objects.create_user(
            email='owner@test.com',
            password='password'
        )

        self.auto_salon = AutoSalonModel.objects.create(
            name="Salon A",
            location="City Center",
            user=self.owner
        )

        self.admin = UserModel.objects.create_user(
            email='admin@test.com',
            password='password'
        )

        self.seller = UserModel.objects.create_user(
            email='seller@test.com',
            password='password'
        )

        self.mechanic = UserModel.objects.create_user(
            email='mechanic@test.com',
            password='password'
        )


        self.salon_role_admin = SalonRoleModels.objects.create(
            user=self.admin,
            auto_salon=self.auto_salon,
            role='admin'
        )

        self.salon_role_seller = SalonRoleModels.objects.create(
            user=self.seller,
            auto_salon=self.auto_salon,
            role='seller'
        )

        self.salon_role_mechanic = SalonRoleModels.objects.create(
            user=self.mechanic,
            auto_salon=self.auto_salon,
            role='mechanic'
        )

    def test_role_assignment(self):
        self.assertEqual(self.salon_role_admin.role, 'admin')
        self.assertEqual(self.salon_role_seller.role, 'seller')
        self.assertEqual(self.salon_role_mechanic.role, 'mechanic')

    def test_is_role_taken(self):
        self.assertTrue(SalonRoleModels.is_role_taken(self.auto_salon, 'admin'))
        self.assertTrue(SalonRoleModels.is_role_taken(self.auto_salon, 'seller'))
        self.assertTrue(SalonRoleModels.is_role_taken(self.auto_salon, 'mechanic'))