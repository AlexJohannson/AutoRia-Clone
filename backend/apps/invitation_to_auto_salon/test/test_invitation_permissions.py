import unittest
from unittest.mock import MagicMock, PropertyMock

from apps.invitation_to_auto_salon.permissions import IsSalonAdminOrSuperUser


class IsSalonAdminOrSuperUserTestCase(unittest.TestCase):

    def setUp(self):
        self.permission = IsSalonAdminOrSuperUser()
        self.view = MagicMock()

    def get_mock_request(self, is_superuser, is_staff, salon_role_exists=False, salon_role_value=None):
        user = MagicMock()
        user.is_superuser = is_superuser
        user.is_staff = is_staff

        if salon_role_exists:
            salon_role = MagicMock()
            salon_role.role = salon_role_value
            type(user).salon_role = PropertyMock(return_value=salon_role)
        else:
            if hasattr(user, 'salon_role'):
                delattr(user, 'salon_role')

        request = MagicMock()
        request.user = user
        return request

    def test_superuser_has_permission(self):
        request = self.get_mock_request(is_superuser=True, is_staff=False)
        self.assertTrue(self.permission.has_permission(request, self.view))

    def test_staff_has_permission(self):
        request = self.get_mock_request(is_superuser=False, is_staff=True)
        self.assertTrue(self.permission.has_permission(request, self.view))

    def test_salon_superuser_has_permission(self):
        request = self.get_mock_request(False, False, True, 'superuser')
        self.assertTrue(self.permission.has_permission(request, self.view))

    def test_salon_admin_has_permission(self):
        request = self.get_mock_request(False, False, True, 'admin')
        self.assertTrue(self.permission.has_permission(request, self.view))

    def test_salon_seller_has_no_permission(self):
        request = self.get_mock_request(False, False, True, 'seller')
        self.assertFalse(self.permission.has_permission(request, self.view))

    def test_salon_mechanic_has_no_permission(self):
        request = self.get_mock_request(False, False, True, 'mechanic')
        self.assertFalse(self.permission.has_permission(request, self.view))

    def test_no_salon_role_no_permission(self):
        request = self.get_mock_request(False, False, False)
        self.assertFalse(self.permission.has_permission(request, self.view))

