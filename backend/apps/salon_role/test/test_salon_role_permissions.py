from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIRequestFactory

from apps.auto_salon.models import AutoSalonModel
from apps.salon_role.models import SalonRoleModels
from apps.salon_role.permissions import CanManageSalonRole, IsSalonMemberOrAdmin

UserModel = get_user_model()

class SalonRolePermissionsTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.salon_owner = UserModel.objects.create_user(
            email='owner@test.com',
            password='password'
        )

        self.auto_salon = AutoSalonModel.objects.create(
            name="Salon A",
            location="City Center",
            user=self.salon_owner
        )

        self.salon_role_owner = SalonRoleModels.objects.create(
            user=self.salon_owner,
            auto_salon=self.auto_salon,
            role='superuser'
        )


        self.admin = UserModel.objects.create_user(
            email='admin@test.com',
            password='password'
        )

        self.salon_role_admin = SalonRoleModels.objects.create(
            user=self.admin,
            auto_salon=self.auto_salon,
            role='admin'
        )


        self.seller = UserModel.objects.create_user(
            email='seller@test.com',
            password='password'
        )

        self.salon_role_seller = SalonRoleModels.objects.create(
            user=self.seller,
            auto_salon=self.auto_salon,
            role='seller'
        )



        self.mechanic = UserModel.objects.create_user(
            email='mechanic@test.com',
            password='password'
        )

        self.salon_role_mechanic = SalonRoleModels.objects.create(
            user=self.mechanic,
            auto_salon=self.auto_salon,
            role='mechanic'
        )


        self.site_superuser = UserModel.objects.create_user(
            email='superuser@test.com',
            password='password',
            is_superuser=True
        )

    def test_is_salon_member_or_admin(self):
        permission = IsSalonMemberOrAdmin()
        request = self.factory.get('/')

        request.user = self.site_superuser
        self.assertTrue(permission.has_permission(request, None))

        request.user = self.admin
        self.assertTrue(permission.has_permission(request, None))

        request.user = self.seller
        self.assertTrue(permission.has_permission(request, None))

        request.user = self.mechanic
        self.assertTrue(permission.has_permission(request, None))

        request.user = self.salon_owner
        self.assertTrue(permission.has_permission(request, None))

        guest_user = UserModel.objects.create_user(email='guest@test.com', password='password')
        request.user = guest_user
        self.assertFalse(permission.has_permission(request, None))

    def test_can_manage_salon_role(self):
        permission = CanManageSalonRole()
        request = self.factory.get('/')

        request.user = self.salon_owner
        self.assertTrue(permission.has_object_permission(request, None, self.salon_role_admin))
        self.assertTrue(permission.has_object_permission(request, None, self.salon_role_seller))
        self.assertTrue(permission.has_object_permission(request, None, self.salon_role_mechanic))
        self.assertTrue(permission.has_object_permission(request, None, self.salon_role_owner))

        request.user = self.admin
        self.assertTrue(permission.has_object_permission(request, None, self.salon_role_seller))
        self.assertTrue(permission.has_object_permission(request, None, self.salon_role_mechanic))
        self.assertTrue(permission.has_object_permission(request, None, self.salon_role_owner))

        request.user = self.seller
        self.assertTrue(permission.has_object_permission(request, None, self.salon_role_seller))
        self.assertFalse(permission.has_object_permission(request, None, self.salon_role_admin))
        self.assertFalse(permission.has_object_permission(request, None, self.salon_role_owner))

        request.user = self.mechanic
        self.assertTrue(permission.has_object_permission(request, None, self.salon_role_mechanic))
        self.assertFalse(permission.has_object_permission(request, None, self.salon_role_admin))
        self.assertFalse(permission.has_object_permission(request, None, self.salon_role_owner))

        request.user = self.site_superuser
        self.assertTrue(permission.has_object_permission(request, None, self.salon_role_owner))
        self.assertTrue(permission.has_object_permission(request, None, self.salon_role_admin))
        self.assertTrue(permission.has_object_permission(request, None, self.salon_role_seller))
        self.assertTrue(permission.has_object_permission(request, None, self.salon_role_mechanic))