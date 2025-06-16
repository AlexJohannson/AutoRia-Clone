from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.auto_salon.models import AutoSalonModel
from apps.premium_account.models import PremiumAccountModel
from apps.salon_role.models import SalonRoleModels
from apps.user.models import ProfileModel, UserModel


class AutoSalonAPITestCase(APITestCase):
    def setUp(self):
        self.owner = UserModel.objects.create_user(
            email='owner@example.com',
            password='ownerpass',
            is_active=True
        )
        self.owner.profile = ProfileModel.objects.create(
            user=self.owner,
            name="Test",
            surname="Test",
            age=30,
            house=10,
            street="Main",
            city="Test",
            region="Test",
            country="Test",
            gender="Male"
        )

        self.admin = UserModel.objects.create_user(
            email='admin@example.com',
            password='adminpass',
            is_active=True,
            is_staff=True
        )
        self.admin.profile = ProfileModel.objects.create(
            user=self.admin,
            name="Test",
            surname="Test",
            age=30,
            house=10,
            street="Main",
            city="Test",
            region="Test",
            country="Test",
            gender="Male"
        )

        self.other_user = UserModel.objects.create_user(
            email='other@example.com',
            password='otherpass',
            is_active=True
        )
        self.other_user.profile = ProfileModel.objects.create(
            user=self.other_user,
            name="Test",
            surname="Test",
            age=30,
            house=10,
            street="Main",
            city="Test",
            region="Test",
            country="Test",
            gender="Male"
        )

        self.auto_salon = AutoSalonModel.objects.create(
            name='Test Salon',
            location='Kyiv',
            user=self.owner
        )

        SalonRoleModels.objects.create(
            user=self.owner,
            auto_salon=self.auto_salon,
            role='superuser'
        )
        PremiumAccountModel.objects.create(auto_salon=self.auto_salon)

    def auth_as(self, user):
        self.client.force_authenticate(user=user)

    def test_get_auto_salon_list_as_admin(self):
        self.auth_as(self.admin)
        url = reverse('auto_salon_create_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        salons_data = response.data.get('data', [])

        self.assertIsInstance(salons_data, list)
        salon_ids = [salon['id'] for salon in salons_data]
        self.assertIn(self.auto_salon.id, salon_ids)

    def test_get_auto_salon_list_as_regular_user(self):
        self.auth_as(self.other_user)
        url = reverse('auto_salon_create_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_auto_salon(self):
        self.auth_as(self.other_user)
        url = reverse('auto_salon_create_list')
        data = {
            'name': 'New Salon',
            'location': 'Lviv'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(AutoSalonModel.objects.filter(name='New Salon').exists())
        self.assertTrue(SalonRoleModels.objects.filter(user=self.other_user, role='superuser').exists())
        self.assertTrue(PremiumAccountModel.objects.filter(auto_salon__name='New Salon').exists())

    def test_create_auto_salon_duplicate(self):
        self.auth_as(self.owner)
        url = reverse('auto_salon_create_list')
        data = {
            'name': 'Duplicate Salon',
            'location': 'Odessa'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_auto_salon(self):
        self.auth_as(self.owner)
        url = reverse('auto_salon_retrieve', args=[self.auto_salon.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.auto_salon.name)

    def test_update_auto_salon(self):
        self.auth_as(self.owner)
        url = reverse('auto_salon_retrieve', args=[self.auto_salon.id])
        data = {
            'name': 'Updated Salon',
            'location': 'Dnipro'
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.auto_salon.refresh_from_db()
        self.assertEqual(self.auto_salon.name, 'Updated Salon')
        self.assertEqual(self.auto_salon.location, 'Dnipro')

    def test_delete_auto_salon(self):
        self.auth_as(self.owner)
        url = reverse('auto_salon_retrieve', args=[self.auto_salon.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(AutoSalonModel.objects.filter(id=self.auto_salon.id).exists())

    def test_forbidden_update_by_non_owner(self):
        self.auth_as(self.other_user)
        url = reverse('auto_salon_retrieve', args=[self.auto_salon.id])
        response = self.client.put(url, data={'name': 'Hacked', 'location': 'Lviv'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_forbidden_delete_by_non_owner(self):
        self.auth_as(self.other_user)
        url = reverse('auto_salon_retrieve', args=[self.auto_salon.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
