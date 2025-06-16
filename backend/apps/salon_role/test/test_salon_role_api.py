from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.auto_salon.models import AutoSalonModel
from apps.salon_role.models import SalonRoleModels
from apps.user.models import ProfileModel, UserModel


class SalonRoleApiTestCase(APITestCase):
    def setUp(self):
        self.superuser = UserModel.objects.create_superuser(
            email='super@test.com',
            password='password'
        )

        self.admin = UserModel.objects.create_user(
            email='admin@test.com',
            password='password'
        )

        self.seller = UserModel.objects.create_user(
            email='seller@test.com',
            password='password'
        )

        self.outsider = UserModel.objects.create_user(
            email='outsider@test.com',
            password='password'
        )


        ProfileModel.objects.create(
            user=self.superuser,
            name='Super User',
            surname='Admin',
            age=35,
            house=10,
            street='Main St',
            city='Big City',
            region='Region',
            country='Country',
            gender='Male'
        )

        ProfileModel.objects.create(
            user=self.admin,
            name='Admin User',
            surname='Admin',
            age=30,
            house=11,
            street='Side St',
            city='Small City',
            region='Region',
            country='Country',
            gender='Female'
        )

        ProfileModel.objects.create(
            user=self.seller,
            name='Seller User',
            surname='Seller',
            age=25,
            house=12,
            street='Market St',
            city='Town',
            region='Region',
            country='Country',
            gender='Male'
        )

        ProfileModel.objects.create(
            user=self.outsider,
            name='Outsider User',
            surname='Visitor',
            age=28,
            house=13,
            street='Random St',
            city='Village',
            region='Region',
            country='Country',
            gender='Female'
        )



        self.auto_salon = AutoSalonModel.objects.create(
            name='Test Salon',
            location='City',
            user=self.superuser
        )


        self.role_superuser = SalonRoleModels.objects.create(
            user=self.superuser,
            auto_salon=self.auto_salon,
            role='superuser'
        )

        self.role_admin = SalonRoleModels.objects.create(
            user=self.admin,
            auto_salon=self.auto_salon,
            role='admin'
        )

        self.role_seller = SalonRoleModels.objects.create(
            user=self.seller,
            auto_salon=self.auto_salon,
            role='seller'
        )

    def test_list_roles_as_member(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('salon_role_list')
        response = self.client.get(url)
        roles = response.data.get('data', [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(r['role'] == 'admin' for r in roles))

    def test_list_roles_as_outsider_forbidden(self):
        self.client.force_authenticate(user=self.outsider)
        url = reverse('salon_role_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_role(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('salon_role_retrieve', kwargs={'pk': self.role_seller.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], 'seller')

    def test_delete_role_self_superuser_deletes_autosalon(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('salon_role_retrieve', kwargs={'pk': self.role_superuser.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(AutoSalonModel.objects.filter(pk=self.auto_salon.pk).exists())

    def test_delete_role_self_non_superuser(self):
        self.client.force_authenticate(user=self.seller)
        url = reverse('salon_role_retrieve', kwargs={'pk': self.role_seller.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(SalonRoleModels.objects.filter(pk=self.role_seller.pk).exists())

    def test_delete_role_other_user(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('salon_role_retrieve', kwargs={'pk': self.role_seller.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(SalonRoleModels.objects.filter(pk=self.role_seller.pk).exists())
