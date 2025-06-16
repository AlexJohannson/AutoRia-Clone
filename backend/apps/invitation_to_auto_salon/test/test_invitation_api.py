from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.auto_salon.models import AutoSalonModel
from apps.invitation_to_auto_salon.models import JoinRequestModel
from apps.salon_role.models import SalonRoleModels
from apps.user.models import ProfileModel, UserModel


class JoinRequestListCreateAPITest(APITestCase):
    def setUp(self):
        JoinRequestModel.objects.all().delete()
        SalonRoleModels.objects.all().delete()
        self.client = APIClient()


        self.user = UserModel.objects.create_user(
            email='user@example.com',
            password='password123'
        )

        self.admin_user = UserModel.objects.create_user(
            email='admin@example.com',
            password='password123'
        )

        self.superuser = UserModel.objects.create_superuser(
            email='superuser@example.com',
            password='password123'
        )

        self.profile = ProfileModel.objects.create(
            name='Test',
            surname='User',
            age=30,
            house=1,
            street='Main Street',
            city='TestCity',
            region='TestRegion',
            country='TestCountry',
            gender='male',
            user=self.user
        )


        self.auto_salon = AutoSalonModel.objects.create(
            name='Test Salon',
            location='Lviv',
            user=self.superuser
        )


        self.admin_role = SalonRoleModels.objects.create(
            user=self.admin_user,
            auto_salon=self.auto_salon,
            role='admin'
        )


        self.join_request = JoinRequestModel.objects.create(
            user=self.user,
            auto_salon=self.auto_salon,
            role='seller',
            status='pending'
        )

        self.url = reverse('join_request_list_create')

    def test_get_join_requests_as_regular_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data.get('data', [])
        self.assertTrue(all(r['user'] == self.user.id for r in data))
        self.assertEqual(len(data), 1)

    def test_get_join_requests_as_salon_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data.get('data', [])
        self.assertTrue(all(int(r['auto_salon']) == self.auto_salon.id for r in data))

    def test_get_join_requests_as_superuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data.get('data', [])
        self.assertGreaterEqual(len(data), 1)

    def test_create_join_request_success(self):
        self.client.force_authenticate(user=self.user)

        data = {'auto_salon': self.auto_salon.id, 'role': 'mechanic'}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.user.id)

        self.assertEqual(int(response.data['auto_salon']), self.auto_salon.id)
        self.assertEqual(response.data['role'], 'mechanic')
        self.assertEqual(response.data['status'], 'pending')

    def test_create_join_request_role_taken(self):
        self.client.force_authenticate(user=self.user)

        data = {'auto_salon': self.auto_salon.id, 'role': 'admin'}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_approve_join_request_success(self):
        self.client.force_authenticate(user=self.admin_user)
        approve_url = reverse('join_request_list_approve', kwargs={'pk': self.join_request.id})
        response = self.client.patch(approve_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Request approved and role assigned')

        role = SalonRoleModels.objects.filter(user=self.user, auto_salon=self.auto_salon, role='seller').first()
        self.assertIsNotNone(role)

        self.join_request.refresh_from_db()
        self.assertEqual(self.join_request.status, 'approved')

    def test_approve_already_processed_request(self):
        self.join_request.status = 'approved'
        self.join_request.save()

        self.client.force_authenticate(user=self.admin_user)
        approve_url = reverse('join_request_list_approve', kwargs={'pk': self.join_request.id})

        response = self.client.patch(approve_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'This request has already been processed')

    def test_approve_request_with_taken_role(self):
        SalonRoleModels.objects.create(
            user=self.superuser,
            auto_salon=self.auto_salon,
            role='seller'
        )

        self.client.force_authenticate(user=self.admin_user)
        approve_url = reverse('join_request_list_approve', kwargs={'pk': self.join_request.id})

        response = self.client.patch(approve_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Role already taken. Request rejected')

        self.join_request.refresh_from_db()
        self.assertEqual(self.join_request.status, 'rejected')

    def test_delete_pending_join_request_success(self):
        self.client.force_authenticate(user=self.admin_user)
        delete_url = reverse('join_request_list_delete', kwargs={'pk': self.join_request.id})

        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(JoinRequestModel.objects.filter(id=self.join_request.id).exists())

    def test_delete_non_pending_join_request_fails(self):
        self.join_request.status = 'approved'
        self.join_request.save()

        self.client.force_authenticate(user=self.admin_user)
        delete_url = reverse('join_request_list_delete', kwargs={'pk': self.join_request.id})

        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(JoinRequestModel.objects.filter(id=self.join_request.id).exists())

