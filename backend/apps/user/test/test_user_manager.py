from unittest import TestCase
from unittest.mock import patch

from apps.user.models import UserModel


class TestUserManager(TestCase):
    def setUp(self):
        self.manager = UserModel.objects

    def test_create_user_missing_email_raises_error(self):
        with self.assertRaises(ValueError):
            self.manager.create_user(email=None, password="12345")

    def test_create_user_missing_password_raises_error(self):
        with self.assertRaises(ValueError):
            self.manager.create_user(email="test@test.com", password=None)

    @patch("apps.user.models.UserModel")
    def test_create_user_success(self, mock_model):
        mock_instance = mock_model.return_value
        mock_instance.set_password.return_value = None
        mock_instance.save.return_value = None

        self.manager.model = mock_model
        user = self.manager.create_user(email="test@test.com", password="12345")
        self.assertEqual(user, mock_instance)

    @patch("apps.user.models.UserModel.objects.create_user")
    def test_create_superuser_sets_flags(self, mock_create_user):
        mock_create_user.return_value = "superuser"
        result = self.manager.create_superuser(email="admin@test.com", password="adminpass")

        self.assertEqual(result, "superuser")
        mock_create_user.assert_called_once()
        kwargs = mock_create_user.call_args.kwargs
        self.assertTrue(kwargs["is_superuser"])
        self.assertTrue(kwargs["is_staff"])
        self.assertTrue(kwargs["is_active"])
        self.assertEqual(kwargs["status"], "active")

