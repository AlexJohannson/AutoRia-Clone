from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase

from apps.user.models import ProfileModel

UserModel = get_user_model()

class UserApiTestCase(APITestCase):
    def setUp(self):
        self.admin = UserModel.objects.create_user(
            email='admin@test.com',
            password='adminpassword',
            is_staff=True,
            is_superuser=True
        )

        self.admin.profile = ProfileModel.objects.create(
            user=self.admin,
            name="Admin",
            surname="Super",
            age=40,
            house=1,
            street="Street",
            city="City",
            region="Region",
            country="Country",
            gender="Male"
        )

        self.user = UserModel.objects.create_user(email='user@test.com', password='userpassword')

        self.user.profile = ProfileModel.objects.create(
            user=self.user,
            name="User",
            surname="Test",
            age=30,
            house=5,
            street="Street",
            city="City",
            region="Region",
            country="Country",
            gender="Male"
        )

        self.client.force_authenticate(user=self.admin)

    def test_user_registration(self):
        new_user_data = {
            "email": "newuser@example.com",
            "password": "securepassword",
            "profile": {
                "name": "New",
                "surname": "User",
                "age": 30,
                "house": 10,
                "street": "Street",
                "city": "City",
                "region": "Region",
                "country": "Country",
                "gender": "Male"
            }
        }

        response = self.client.post(reverse('user_create'), new_user_data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(UserModel.objects.filter(email="newuser@example.com").exists())

    def test_get_users_list(self):
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)

    def test_user_detail_update_delete(self):
        response = self.client.get(reverse(
            'user_detail_profile',
            kwargs={'pk': self.user.id}))

        self.assertEqual(response.status_code, 200)

        update_data = {
            "email": self.user.email,
            "password": "newpassword123",
            "profile": {
                "id": self.user.profile.id,
                "name": "Updated",
                "surname": "Updated",
                "age": 36,
                "house": 10,
                "street": "Updated",
                "city": "Updated",
                "region": "Updated",
                "country": "Updated",
                "gender": "Male"
            }
        }
        response = self.client.put(reverse(
            'user_detail_profile',
            kwargs={'pk': self.user.id}),
            update_data,
            format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(reverse(
            'user_detail_profile',
            kwargs={'pk': self.user.id}))

        self.assertEqual(response.status_code, 204)

    def test_block_unblock_user(self):
        user_id = self.user.id
        block_data = {"action": "block"}
        response = self.client.patch(reverse(
            'user_block_unblock',
            kwargs={'pk': user_id}),
            block_data,
            format="json"
        )
        self.assertEqual(response.status_code, 200)

        unblock_data = {"action": "unblock"}
        response = self.client.patch(reverse(
            'user_block_unblock',
            kwargs={'pk': user_id}),
            unblock_data,
            format="json"
        )
        self.assertEqual(response.status_code, 200)

    def test_make_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(reverse(
            'user_to_admin',
            kwargs={'pk': self.user.id}),
            format="json"
        )
        self.assertEqual(response.status_code, 200)

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_staff)




