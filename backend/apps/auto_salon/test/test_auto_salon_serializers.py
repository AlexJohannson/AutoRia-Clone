from django.test import TestCase

from apps.auto_salon.models import AutoSalonModel
from apps.auto_salon.serializers import AutoSalonSerializer
from apps.user.models import UserModel


class AutoSalonSerializerTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(email='testuser@example.com', is_active=True)
        self.user.set_password('testpassword')
        self.user.save()

        self.auto_salon = AutoSalonModel.objects.create(
            name='Fast Cars',
            location='Kyiv',
            user=self.user
        )

    def test_serialization(self):
        serializer = AutoSalonSerializer(self.auto_salon)
        expected_data = {
            'id': self.auto_salon.id,
            'name': 'Fast Cars',
            'location': 'Kyiv',
            'user': self.user.id,
            'created_at': serializer.data['created_at']
        }
        self.assertEqual(serializer.data, expected_data)

    def test_deserialization_valid_data(self):
        valid_data = {
            'name': 'Luxury Wheels',
            'location': 'Lviv',
        }
        serializer = AutoSalonSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_read_only_fields(self):
        invalid_data = {
            'id': 999,
            'name': 'New Name',
            'location': 'New Location',
            'user': 100,
            'created_at': '2024-01-01T00:00:00Z'
        }
        serializer = AutoSalonSerializer(
            instance=self.auto_salon,
            data=invalid_data,
            partial=True
        )
        self.assertTrue(serializer.is_valid())

        updated_instance = serializer.save()

        self.assertNotEqual(updated_instance.id, 999)
        self.assertNotEqual(updated_instance.user.id, 100)
        self.assertNotEqual(str(updated_instance.created_at), '2024-01-01T00:00:00Z')

        self.assertEqual(updated_instance.name, 'New Name')
        self.assertEqual(updated_instance.location, 'New Location')
