from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIRequestFactory

from apps.sellers.models import SellersModel
from apps.sellers.permissions import IsAdminOrSuperuser, IsSellerOrAdmin

UserModel = get_user_model()

class PermissionsTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserModel.objects.create_user(
            email='user@example.com',
            password='password'
        )

        self.admin = UserModel.objects.create_user(
            email='admin@example.com',
            password='password',
            is_staff=True
        )

        self.superuser = UserModel.objects.create_user(
            email='super@example.com',
            password='password',
            is_staff=True,
            is_superuser=True
        )

        self.seller = SellersModel.objects.create(user=self.user)
        self.seller_permission = IsSellerOrAdmin()
        self.admin_permission = IsAdminOrSuperuser()

    def test_seller_access(self):
        request = self.factory.get('/')
        request.user = self.user
        self.assertTrue(self.seller_permission.has_object_permission(request, None, self.seller))

    def test_admin_access_seller(self):
        request = self.factory.get('/')
        request.user = self.admin
        self.assertTrue(self.seller_permission.has_object_permission(request, None, self.seller))

    def test_superuser_access_seller(self):
        request = self.factory.get('/')
        request.user = self.superuser
        self.assertTrue(self.seller_permission.has_object_permission(request, None, self.seller))

    def test_unauthorized_access_seller(self):
        another_user = UserModel.objects.create_user(email='other@example.com', password='password')
        request = self.factory.get('/')
        request.user = another_user
        self.assertFalse(self.seller_permission.has_object_permission(request, None, self.seller))

    def test_admin_or_superuser_access(self):
        request_admin = self.factory.get('/')
        request_admin.user = self.admin
        self.assertTrue(self.admin_permission.has_permission(request_admin, None))

        request_superuser = self.factory.get('/')
        request_superuser.user = self.superuser
        self.assertTrue(self.admin_permission.has_permission(request_superuser, None))

    def test_unauthorized_access_admin(self):
        request = self.factory.get('/')
        request.user = self.user
        self.assertFalse(self.admin_permission.has_permission(request, None))