from unittest.mock import MagicMock, patch

from django.test import TestCase

from apps.auto_salon_listings.permissions import IsAdminOrSuperuser, IsSalonStaffOrAdmin


class PermissionTestCase(TestCase):
    def setUp(self):
        self.request = MagicMock()
        self.view = MagicMock()

    def test_is_admin_or_superuser_with_staff(self):
        self.request.user.is_staff = True
        self.request.user.is_superuser = False

        permission = IsAdminOrSuperuser()
        self.assertTrue(permission.has_permission(self.request, self.view))

    def test_is_admin_or_superuser_with_superuser(self):
        self.request.user.is_staff = False
        self.request.user.is_superuser = True

        permission = IsAdminOrSuperuser()
        self.assertTrue(permission.has_permission(self.request, self.view))

    def test_is_admin_or_superuser_denied(self):
        self.request.user.is_staff = False
        self.request.user.is_superuser = False

        permission = IsAdminOrSuperuser()
        self.assertFalse(permission.has_permission(self.request, self.view))

    def test_is_salon_staff_or_admin_superuser(self):
        self.request.user.is_authenticated = True
        self.request.user.is_superuser = True
        self.request.user.is_staff = False

        permission = IsSalonStaffOrAdmin()
        self.assertTrue(permission.has_permission(self.request, self.view))

    def test_is_salon_staff_or_admin_staff(self):
        self.request.user.is_authenticated = True
        self.request.user.is_superuser = False
        self.request.user.is_staff = True

        permission = IsSalonStaffOrAdmin()
        self.assertTrue(permission.has_permission(self.request, self.view))

    def test_is_salon_staff_or_admin_not_authenticated(self):
        self.request.user.is_authenticated = False

        permission = IsSalonStaffOrAdmin()
        self.assertFalse(permission.has_permission(self.request, self.view))

    @patch('apps.salon_role.permissions.SalonRoleModels.objects.filter')
    def test_is_salon_staff_or_admin_salon_role_exists(self, mock_filter):
        self.request.user.is_authenticated = True
        self.request.user.is_superuser = False
        self.request.user.is_staff = False

        mock_query = MagicMock()
        mock_query.filter.return_value.exists.return_value = True
        mock_filter.return_value = mock_query

        permission = IsSalonStaffOrAdmin()
        self.assertTrue(permission.has_permission(self.request, self.view))

        mock_filter.assert_called_once_with(user=self.request.user)
        mock_query.filter.assert_called_once_with(role__in=['superuser', 'admin', 'seller'])

    @patch('apps.salon_role.permissions.SalonRoleModels.objects.filter')
    def test_is_salon_staff_or_admin_salon_role_not_exists(self, mock_filter):
        self.request.user.is_authenticated = True
        self.request.user.is_superuser = False
        self.request.user.is_staff = False

        mock_query = MagicMock()
        mock_query.filter.return_value.exists.return_value = False
        mock_filter.return_value = mock_query

        permission = IsSalonStaffOrAdmin()
        self.assertFalse(permission.has_permission(self.request, self.view))

        mock_filter.assert_called_once_with(user=self.request.user)
        mock_query.filter.assert_called_once_with(role__in=['superuser', 'admin', 'seller'])
