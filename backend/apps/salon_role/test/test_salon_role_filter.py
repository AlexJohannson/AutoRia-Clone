from django.test import TestCase

from apps.auto_salon.models import AutoSalonModel
from apps.salon_role.filetr import SalonRoleFilter
from apps.salon_role.models import SalonRoleModels
from apps.user.models import UserModel


class SalonRoleFilterTestCase(TestCase):
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

    def test_filter_by_role(self):
        queryset = SalonRoleModels.objects.all()
        filtered = SalonRoleFilter({'role': 'seller'}, queryset=queryset).qs

        self.assertEqual(filtered.count(), 1)
        self.assertEqual(filtered.first().role, 'seller')

    def test_ordering_by_id(self):
        queryset = SalonRoleModels.objects.all()
        ordered = SalonRoleFilter({'order': 'id'}, queryset=queryset).qs

        sorted_ids = list(queryset.order_by('id').values_list('id', flat=True))
        filtered_ids = list(ordered.values_list('id', flat=True))

        self.assertEqual(filtered_ids, sorted_ids)