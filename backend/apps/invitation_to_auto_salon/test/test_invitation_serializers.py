from django.test import RequestFactory, TestCase

from rest_framework.exceptions import ValidationError

from apps.auto_salon.models import AutoSalonModel
from apps.invitation_to_auto_salon.serializers import JoinRequestSerializer
from apps.salon_role.models import SalonRoleModels
from apps.user.models import UserModel


class JoinRequestSerializerTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserModel.objects.create_user(email='test@example.com', password='pass1234')

        self.auto_salon = AutoSalonModel.objects.create(
            name='Test Auto Salon',
            location='Kyiv',
            user=self.user
        )
        self.context = {
            'request': self.factory.post('/', {}, content_type='application/json')
        }
        self.context['request'].user = self.user

    def test_serializer_valid_data(self):
        data = {
            'auto_salon': self.auto_salon.id,
            'role': 'seller'
        }

        serializer = JoinRequestSerializer(data=data, context=self.context)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()

        self.assertEqual(instance.user, self.user)
        self.assertEqual(instance.auto_salon, self.auto_salon)
        self.assertEqual(instance.role, 'seller')
        self.assertEqual(instance.status, 'pending')

    def test_serializer_role_taken(self):
        SalonRoleModels.objects.create(
            user=self.user,
            auto_salon=self.auto_salon,
            role='seller'
        )

        data = {
            'auto_salon': self.auto_salon.id,
            'role': 'seller'
        }

        serializer = JoinRequestSerializer(data=data, context=self.context)

        with self.assertRaises(ValidationError) as e:
            serializer.is_valid(raise_exception=True)

        self.assertIn('role', str(e.exception))
