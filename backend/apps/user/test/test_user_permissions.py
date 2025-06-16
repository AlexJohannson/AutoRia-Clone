from unittest import TestCase
from unittest.mock import MagicMock

from apps.user.permissions import IsAdminOrSuperuser, IsOwnerOrAdmin, IsSuperUserOnly


class TestPermissions(TestCase):

    def test_is_admin_or_superuser_allows_admin(self):
        request = MagicMock()
        request.user.is_staff = True
        request.user.is_superuser = False
        assert IsAdminOrSuperuser().has_permission(request, None) is True

    def test_is_admin_or_superuser_allows_superuser(self):
        request = MagicMock()
        request.user.is_staff = False
        request.user.is_superuser = True
        assert IsAdminOrSuperuser().has_permission(request, None) is True

    def test_is_admin_or_superuser_denies_user(self):
        request = MagicMock()
        request.user.is_staff = False
        request.user.is_superuser = False
        assert IsAdminOrSuperuser().has_permission(request, None) is False

    def test_is_owner_or_admin_allows_owner(self):
        request = MagicMock()
        user = MagicMock()
        request.user = user
        assert IsOwnerOrAdmin().has_object_permission(request, None, user) is True

    def test_is_owner_or_admin_allows_admin(self):
        request = MagicMock()
        request.user = MagicMock(is_staff=True, is_superuser=False)
        obj = MagicMock()
        assert IsOwnerOrAdmin().has_object_permission(request, None, obj) is True

    def test_is_super_user_only_allows(self):
        request = MagicMock()
        request.user.is_authenticated = True
        request.user.is_superuser = True
        assert IsSuperUserOnly().has_permission(request, None) is True

    def test_is_super_user_only_denies(self):
        request = MagicMock()
        request.user.is_authenticated = True
        request.user.is_superuser = False
        assert IsSuperUserOnly().has_permission(request, None) is False
