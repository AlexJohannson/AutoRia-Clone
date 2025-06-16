from django.test import TestCase

from rest_framework.serializers import ValidationError

from apps.auto_salon.models import AutoSalonModel
from apps.salon_role.models import SalonRoleModels
from apps.salon_role.serializers import SalonRoleSerializer
from apps.user.models import UserModel


class SalonRoleSerializerTestCase(TestCase):
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

    def test_validate_existing_role(self):
        another_user = UserModel.objects.create_user(
            email='another@test.com',
            password='password'
        )

        attrs = {
            'user': another_user,
            'auto_salon': self.auto_salon,
            'role': 'seller',
        }

        serializer = SalonRoleSerializer()
        with self.assertRaises(ValidationError) as context:
            serializer.validate(attrs)
        self.assertTrue(
            any('already exists' in str(err) for err in context.exception.detail))

