from unittest import TestCase
from unittest.mock import MagicMock

from apps.listings.permissions import IsAdminOrSuperUser, IsOwnerOrAdmin


class TestListingsPermissions(TestCase):

    def test_is_admin_or_superuser_allows_admin(self):
        request = MagicMock()
        request.user = MagicMock(is_staff=True, is_superuser=False)
        assert IsAdminOrSuperUser().has_permission(request, None) is True

    def test_is_admin_or_superuser_allows_superuser(self):
        request = MagicMock()
        request.user = MagicMock(is_staff=False, is_superuser=True)
        assert IsAdminOrSuperUser().has_permission(request, None) is True

    def test_is_admin_or_superuser_denies_user(self):
        request = MagicMock()
        request.user = MagicMock(is_staff=False, is_superuser=False)
        assert IsAdminOrSuperUser().has_permission(request, None) is False

    def test_is_owner_or_admin_allows_admin(self):
        user = MagicMock(is_staff=True, is_superuser=False)
        request = MagicMock(user=user)
        obj = MagicMock(seller=MagicMock(user=MagicMock()))
        assert IsOwnerOrAdmin().has_object_permission(request, None, obj) is True

    def test_is_owner_or_admin_allows_superuser(self):
        user = MagicMock(is_staff=False, is_superuser=True)
        request = MagicMock(user=user)
        obj = MagicMock(seller=MagicMock(user=MagicMock()))
        assert IsOwnerOrAdmin().has_object_permission(request, None, obj) is True

    def test_is_owner_or_admin_allows_seller(self):
        user = MagicMock()
        request = MagicMock(user=user)
        obj = MagicMock(seller=MagicMock(user=user))
        assert IsOwnerOrAdmin().has_object_permission(request, None, obj) is True

    def test_is_owner_or_admin_other_user(self):
        user = MagicMock(is_staff=False, is_superuser=False)
        not_owner_user = MagicMock()
        not_owner_user.__eq__.return_value = False
        request = MagicMock(user=user)
        obj = MagicMock(seller=MagicMock(user=not_owner_user))
        user.__eq__.return_value = False
        assert IsOwnerOrAdmin().has_object_permission(request, None, obj) is False


