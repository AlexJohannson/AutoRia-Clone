from unittest import TestCase
from unittest.mock import MagicMock

from apps.car_brand.permissions import IsAdminOrSuperUser


class IsAdminOrSuperUserTest(TestCase):
    def setUp(self):
        self.permission = IsAdminOrSuperUser()

    def test_has_permission_superuser(self):
        request = MagicMock()
        request.user.is_superuser = True
        request.user.is_staff = False
        self.assertTrue(self.permission.has_permission(request, None))

    def test_has_permission_staff(self):
        request = MagicMock()
        request.user.is_superuser = False
        request.user.is_staff = True
        self.assertTrue(self.permission.has_permission(request, None))

    def test_has_permission_neither(self):
        request = MagicMock()
        request.user.is_superuser = False
        request.user.is_staff = False
        self.assertFalse(self.permission.has_permission(request, None))
