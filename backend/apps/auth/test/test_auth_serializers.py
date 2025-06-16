from django.test import TestCase

from apps.auth.serializers import EmailSerializers, PasswordSerializer, UserRoleSerializer
from apps.user.models import UserModel


class UserSerializersTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='testuser@example.com',
            password='StrongPassword123'
        )

    def test_email_serializer_valid(self):
        data = {'email': 'valid@example.com'}
        serializer = EmailSerializers(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['email'], data['email'])

    def test_email_serializer_invalid(self):
        data = {'email': 'invalid-email'}
        serializer = EmailSerializers(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_password_serializer_valid(self):
        data = {'password': 'NewPassword123'}
        serializer = PasswordSerializer(instance=self.user, data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['password'], data['password'])

    def test_password_serializer_invalid_missing_password(self):
        data = {}
        serializer = PasswordSerializer(instance=self.user, data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_user_role_serializer_valid(self):
        data = {
            'is_staff': True,
            'is_user': False,
            'is_seller': True,
            'is_auto_salon_member': False
        }
        serializer = UserRoleSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['is_staff'], data['is_staff'])
        self.assertEqual(serializer.validated_data['is_user'], data['is_user'])
        self.assertEqual(serializer.validated_data['is_seller'], data['is_seller'])
        self.assertEqual(serializer.validated_data['is_auto_salon_member'], data['is_auto_salon_member'])

    def test_user_role_serializer_invalid_missing_fields(self):
        data = {
            'is_staff': True,
            'is_user': False
        }
        serializer = UserRoleSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('is_seller', serializer.errors)
        self.assertIn('is_auto_salon_member', serializer.errors)
