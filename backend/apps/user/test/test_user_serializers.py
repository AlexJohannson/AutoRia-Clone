from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.user.models import ProfileModel
from apps.user.serializers import UserSerializer

UserModel = get_user_model()


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(email='testuser@example.com', password='password')

        self.profile = ProfileModel.objects.create(
            user=self.user,
            name="Test",
            surname="User",
            age=30,
            house=5,
            street="Main Street",
            city="Kyiv",
            region="Kyivska",
            country="Ukraine",
            gender="Male"
        )

    def test_user_serializer_valid_data(self):
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'profile': {
                'name': 'New',
                'surname': 'User',
                'age': 25,
                'house': 10,
                'street': 'Newstreet',
                'city': 'Lviv',
                'region': 'Lvivska',
                'country': 'Ukraine',
                'gender': 'Female'
            }
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_user_serializer_create(self):
        data = {
            'email': 'createduser@example.com',
            'password': 'password123',
            'profile': {
                'name': 'Created',
                'surname': 'User',
                'age': 28,
                'house': 3,
                'street': 'Createdstreet',
                'city': 'Odesa',
                'region': 'Odeska',
                'country': 'Ukraine',
                'gender': 'Male'
            }
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.profile.name, data['profile']['name'])

    def test_user_serializer_update(self):
        update_data = {
            'profile': {
                'name': 'Updated',
                'surname': 'Updatedsurname',
                'age': 35,
                'street': 'Updatedstreet',
                'house': 15,
                'city': 'Updatedcity',
                'region': 'Updatedregion',
                'country': 'Updatedcountry',
                'gender': 'Male'
            }
        }
        serializer = UserSerializer(instance=self.user, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.profile.name, update_data['profile']['name'])
        self.assertEqual(user.profile.street, update_data['profile']['street'])


    def test_invalid_user_serializer(self):
        invalid_data = {
            'email': 'invaliduser@example.com',
            'password': 'password123',
            'profile': {
                'name': '',
                'surname': '',
                'age': 'invalid_age',
                'house': 'not_a_number',
            }
        }
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('profile', serializer.errors)

