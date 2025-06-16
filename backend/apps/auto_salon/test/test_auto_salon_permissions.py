from unittest import TestCase
from unittest.mock import MagicMock

from apps.auto_salon.permissions import IsAdminOrSuperUser, IsSalonOwnerAdminOrSuperuser


class PermissionsTest(TestCase):
    def setUp(self):
        self.admin_or_superuser_permission = IsAdminOrSuperUser()
        self.salon_owner_admin_or_superuser_permission = IsSalonOwnerAdminOrSuperuser()

    def build_request(self, is_authenticated=True, is_superuser=False, is_staff=False, salon_role=None):
        request = MagicMock()
        request.user.is_authenticated = is_authenticated
        request.user.is_superuser = is_superuser
        request.user.is_staff = is_staff
        request.user.salon_role = salon_role
        return request

    def build_salon_role(self, salon_id, role):
        salon_role = MagicMock()
        salon_role.auto_salon.id = salon_id
        salon_role.role = role
        return salon_role


    def test_admin_or_superuser_permission_superuser_has_access(self):
        request = self.build_request(is_superuser=True)
        self.assertTrue(self.admin_or_superuser_permission.has_permission(request, None))

    def test_admin_or_superuser_permission_staff_has_access(self):
        request = self.build_request(is_staff=True)
        self.assertTrue(self.admin_or_superuser_permission.has_permission(request, None))

    def test_admin_or_superuser_permission_normal_user_no_access(self):
        request = self.build_request(is_superuser=False, is_staff=False)
        self.assertFalse(self.admin_or_superuser_permission.has_permission(request, None))


    def test_salon_permission_authenticated_user_has_permission(self):
        request = self.build_request(is_authenticated=True)
        self.assertTrue(self.salon_owner_admin_or_superuser_permission.has_permission(request, None))

    def test_salon_permission_unauthenticated_user_no_permission(self):
        request = self.build_request(is_authenticated=False)
        self.assertFalse(self.salon_owner_admin_or_superuser_permission.has_permission(request, None))

    def test_salon_permission_superuser_has_object_permission(self):
        request = self.build_request(is_superuser=True)

        obj = MagicMock()
        obj.id = 1

        self.assertTrue(self.salon_owner_admin_or_superuser_permission.has_object_permission(request, None, obj))

    def test_salon_permission_staff_has_object_permission(self):
        request = self.build_request(is_staff=True)

        obj = MagicMock()
        obj.id = 1

        self.assertTrue(self.salon_owner_admin_or_superuser_permission.has_object_permission(request, None, obj))

    def test_salon_permission_salon_superuser_to_own_salon(self):
        salon_role = self.build_salon_role(salon_id=1, role='superuser')
        request = self.build_request(salon_role=salon_role)

        obj = MagicMock()
        obj.id = 1

        self.assertTrue(self.salon_owner_admin_or_superuser_permission.has_object_permission(request, None, obj))

    def test_salon_permission_salon_admin_to_own_salon(self):
        salon_role = self.build_salon_role(salon_id=1, role='admin')
        request = self.build_request(salon_role=salon_role)

        obj = MagicMock()
        obj.id = 1

        self.assertTrue(self.salon_owner_admin_or_superuser_permission.has_object_permission(request, None, obj))

    def test_salon_permission_salon_superuser_to_other_salon(self):
        salon_role = self.build_salon_role(salon_id=2, role='superuser')
        request = self.build_request(salon_role=salon_role)

        obj = MagicMock()
        obj.id = 1

        self.assertFalse(self.salon_owner_admin_or_superuser_permission.has_object_permission(request, None, obj))

    def test_salon_permission_salon_admin_to_other_salon(self):
        salon_role = self.build_salon_role(salon_id=2, role='admin')
        request = self.build_request(salon_role=salon_role)

        obj = MagicMock()
        obj.id = 1

        self.assertFalse(self.salon_owner_admin_or_superuser_permission.has_object_permission(request, None, obj))

    def test_salon_permission_salon_user_with_low_role_no_access(self):
        salon_role = self.build_salon_role(salon_id=1, role='seller')
        request = self.build_request(salon_role=salon_role)

        obj = MagicMock()
        obj.id = 1

        self.assertFalse(self.salon_owner_admin_or_superuser_permission.has_object_permission(request, None, obj))

    def test_salon_permission_user_without_salon_role_no_access(self):
        request = self.build_request()
        if hasattr(request.user, 'salon_role'):
            del request.user.salon_role

        obj = MagicMock()
        obj.id = 1

        self.assertFalse(self.salon_owner_admin_or_superuser_permission.has_object_permission(request, None, obj))

