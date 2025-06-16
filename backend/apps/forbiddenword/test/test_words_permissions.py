import unittest
from unittest.mock import MagicMock

from apps.forbiddenword.permissions import IsAdminOrSuperuser


class TestIsAdminOrSuperuser(unittest.TestCase):

    def setUp(self):
        self.permission = IsAdminOrSuperuser()

    def test_user_is_staff(self):
        mock_user = MagicMock()
        mock_user.is_staff = True
        mock_user.is_superuser = False

        mock_request = MagicMock()
        mock_request.user = mock_user

        self.assertTrue(self.permission.has_permission(mock_request, None))

    def test_user_is_superuser(self):
        mock_user = MagicMock()
        mock_user.is_staff = False
        mock_user.is_superuser = True

        mock_request = MagicMock()
        mock_request.user = mock_user

        self.assertTrue(self.permission.has_permission(mock_request, None))

    def test_user_is_neither(self):
        mock_user = MagicMock()
        mock_user.is_staff = False
        mock_user.is_superuser = False

        mock_request = MagicMock()
        mock_request.user = mock_user

        self.assertFalse(self.permission.has_permission(mock_request, None))

    def test_no_user(self):
        mock_request = MagicMock()
        mock_request.user = None

        self.assertFalse(self.permission.has_permission(mock_request, None))