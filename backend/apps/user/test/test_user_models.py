from unittest import TestCase

from apps.user.models import UserModel


class TestUserModel(TestCase):

    def test_username_field_is_email(self):
        self.assertEqual(UserModel.USERNAME_FIELD, "email")

    def test_user_model_default_status(self):
        user = UserModel()
        self.assertEqual(user.status, "active")

    def test_user_model_default_flags(self):
        user = UserModel()
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
